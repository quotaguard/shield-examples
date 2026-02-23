"""
quotaguard.py — drop this file into your project unchanged.

Call configure_socks_proxy() once at the very top of your entry point,
before importing pymongo or any other network library.
"""

import contextlib
import errno as _errno
import os
import socket as _socket
import ssl
import struct
import threading
from urllib.parse import urlparse


# ── SOCKS5 helpers ──────────────────────────────────────────────────────────────

def _recv_exact(sock, n):
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise RuntimeError("SOCKS5: connection closed unexpectedly during handshake")
        buf += chunk
    return buf


def _socks5_connect(tls_sock, host, port, username, password):
    """Perform a SOCKS5 CONNECT handshake with username/password auth over tls_sock."""
    # Greeting
    tls_sock.sendall(b"\x05\x01\x02")
    resp = _recv_exact(tls_sock, 2)
    if resp[0:1] != b"\x05" or resp[1:2] != b"\x02":
        raise RuntimeError(
            f"SOCKS5: unexpected greeting response: {resp!r}"
        )

    # Username/password auth (RFC 1929)
    u = username.encode("utf-8") if isinstance(username, str) else username
    p = password.encode("utf-8") if isinstance(password, str) else password
    tls_sock.sendall(b"\x01" + bytes([len(u)]) + u + bytes([len(p)]) + p)
    if _recv_exact(tls_sock, 2)[1:2] != b"\x00":
        raise RuntimeError("SOCKS5: authentication failed (wrong username/password?)")

    # CONNECT request
    h = host.encode("utf-8") if isinstance(host, str) else host
    tls_sock.sendall(
        b"\x05\x01\x00\x03" + bytes([len(h)]) + h + struct.pack(">H", port)
    )

    # Response
    hdr = _recv_exact(tls_sock, 4)
    if hdr[1:2] != b"\x00":
        codes = {1:"general failure",2:"not allowed",3:"network unreachable",
                 4:"host unreachable",5:"connection refused"}
        raise RuntimeError(
            f"SOCKS5: CONNECT to {host}:{port} failed: "
            f"{codes.get(hdr[1], f'error {hdr[1]:#x}')}"
        )

    # Consume bound-address from response
    atyp = hdr[3]
    if   atyp == 0x01: _recv_exact(tls_sock, 6)
    elif atyp == 0x03: _recv_exact(tls_sock, _recv_exact(tls_sock, 1)[0] + 2)
    elif atyp == 0x04: _recv_exact(tls_sock, 18)


# ── ShieldSocket ────────────────────────────────────────────────────────────────

_PROXY_HOST = None
_PROXY_PORT = 1081
_PROXY_USERNAME = None
_PROXY_PASSWORD = None
_REAL_SOCKET = None


class ShieldSocket(_socket.socket):
    """
    Transparently tunnels connections through QuotaGuard Shield (SOCKS5-over-TLS).

    Uses a Unix-domain socketpair + two daemon threads to bridge PyMongo's socket
    through a TLS connection to the Shield proxy. PyMongo (including its own MongoDB
    TLS layer) never needs to know about the proxy.
    """

    def __init__(self, family=_socket.AF_INET, type=_socket.SOCK_STREAM,
                 proto=0, fileno=None):
        if fileno is not None:
            super().__init__(fileno=fileno)
            self._inner = None
            self._tls_sock = None
            return
        outer, inner = _socket.socketpair(_socket.AF_UNIX, _socket.SOCK_STREAM)
        super().__init__(fileno=outer.detach())
        self._inner = inner
        self._tls_sock = None

    def connect(self, address):
        host, port = address
        raw = _REAL_SOCKET(_socket.AF_INET, _socket.SOCK_STREAM)
        raw.connect((_PROXY_HOST, _PROXY_PORT))
        ctx = ssl.create_default_context()
        ctx.minimum_version = ssl.TLSVersion.TLSv1_2
        self._tls_sock = ctx.wrap_socket(raw, server_hostname=_PROXY_HOST)
        _socks5_connect(self._tls_sock, host, port, _PROXY_USERNAME, _PROXY_PASSWORD)
        self._start_bridge()

    def _start_bridge(self):
        def pump(src, dst):
            try:
                while True:
                    data = src.recv(65536)
                    if not data:
                        break
                    dst.sendall(data)
            except Exception:
                pass
            finally:
                for s in (src, dst):
                    with contextlib.suppress(Exception): s.shutdown(_socket.SHUT_RDWR)
                    with contextlib.suppress(Exception): s.close()

        for args in [(self._inner, self._tls_sock), (self._tls_sock, self._inner)]:
            threading.Thread(target=pump, args=args, daemon=True).start()

    def setsockopt(self, level, optname, value, optlen=None):
        # Unix socketpair doesn't support TCP-level options; ignore them safely.
        try:
            return super().setsockopt(level, optname, value) if optlen is None \
                else super().setsockopt(level, optname, value, optlen)
        except OSError as exc:
            if exc.errno == _errno.EOPNOTSUPP:
                return
            raise

    def close(self):
        super().close()
        for s in (self._inner, self._tls_sock):
            with contextlib.suppress(Exception):
                if s: s.close()


# ── Public API ──────────────────────────────────────────────────────────────────

def configure_socks_proxy():
    """
    Parse QUOTAGUARDSHIELD_URL and install ShieldSocket as the global socket class.
    Must be called before importing pymongo or any other network library.
    """
    global _PROXY_HOST, _PROXY_PORT, _PROXY_USERNAME, _PROXY_PASSWORD, _REAL_SOCKET

    proxy_url = os.getenv("QUOTAGUARDSHIELD_URL") or os.getenv("QGSHIELD_URL")
    if not proxy_url:
        raise RuntimeError(
            "Set QUOTAGUARDSHIELD_URL to your QuotaGuard Shield proxy URL, e.g.:\n"
            "  https://user:password@us-east-shield-01.quotaguard.com:9294"
        )

    parsed = urlparse(proxy_url)
    if not parsed.hostname or not parsed.username or not parsed.password:
        raise RuntimeError(f"Could not parse host/credentials from: {proxy_url!r}")

    _PROXY_HOST     = parsed.hostname
    _PROXY_PORT     = 1081   # Shield always uses SOCKS5-over-TLS on port 1081
    _PROXY_USERNAME = parsed.username
    _PROXY_PASSWORD = parsed.password

    _REAL_SOCKET    = _socket.socket   # save original before patching
    _socket.socket  = ShieldSocket

    # PyMongo ORs SOCK_CLOEXEC into the socket type; ssl rejects the result.
    if hasattr(_socket, "SOCK_CLOEXEC"):
        del _socket.SOCK_CLOEXEC
