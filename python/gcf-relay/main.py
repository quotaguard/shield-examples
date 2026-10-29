import os
import urllib3
from urllib.parse import urlparse, unquote
import functions_framework

# QUOTAGUARDSHIELD_URL is https://user:pass@<region>-shield-01.quotaguard.com:9294.
# The hop from this function to the proxy is TLS; the request to the target is
# tunneled through it unchanged. urllib3 does not send credentials embedded
# in the proxy URL, so split them out and pass explicit Proxy-Authorization headers.
qg = urlparse(os.environ["QUOTAGUARDSHIELD_URL"])
proxy = urllib3.ProxyManager(
    f"{qg.scheme}://{qg.hostname}:{qg.port}",
    proxy_headers=urllib3.make_headers(
        proxy_basic_auth=f"{unquote(qg.username)}:{unquote(qg.password)}"
    ),
)


@functions_framework.http
def relay(request):
    headers = {name.lower(): value for name, value in request.headers.items()}

    # Reject calls that don't carry your secret key
    if headers.get("x-relay-key") != os.environ["RELAY_KEY"]:
        return ("Forbidden", 403)

    target = headers.get("x-target-url")
    if not target:
        return ("Missing X-Target-URL header", 400)

    # Pass through the headers the target API needs
    fwd = {}
    for name in ("content-type", "authorization", "accept"):
        if name in headers:
            fwd[name] = headers[name]
    # Any header you prefix with "x-fwd-" is forwarded without the prefix
    # (e.g. X-Fwd-X-Api-Key: abc arrives at the target as X-Api-Key: abc).
    for name, value in headers.items():
        if name.startswith("x-fwd-"):
            fwd[name[6:]] = value

    resp = proxy.request(
        request.method, target, body=request.get_data() or None, headers=fwd, timeout=30.0
    )
    return (
        resp.data,
        resp.status,
        {"Content-Type": resp.headers.get("Content-Type", "application/json")},
    )
