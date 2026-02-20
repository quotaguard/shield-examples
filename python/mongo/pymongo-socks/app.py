"""
MongoDB (PyMongo) via QuotaGuard Shield — no QGTunnel.

Copy quotaguard.py into your project, then follow the same three-step pattern
shown here: call configure_socks_proxy(), import MongoClient, write your app.

Environment variables:
    QUOTAGUARDSHIELD_URL  https://user:password@...quotaguard.com:9294
    MONGO_URI             mongodb://user:password@host1:27017,.../?ssl=true&...

Note: mongodb+srv:// URIs are not supported — see the README for how to convert.
"""

import os

# ── Step 1: patch the socket layer BEFORE importing pymongo ─────────────────────
from quotaguard import configure_socks_proxy
configure_socks_proxy()

# ── Step 2: now it's safe to import pymongo ─────────────────────────────────────
from pymongo import MongoClient


# ── Step 3: write your application as normal ────────────────────────────────────
def main():
    mongo_uri = os.environ.get("MONGO_URI")
    if not mongo_uri:
        raise RuntimeError("Set MONGO_URI to a standard mongodb:// connection string.")

    if mongo_uri.startswith("mongodb+srv://"):
        raise RuntimeError(
            "mongodb+srv:// URIs are not supported — DNS SRV lookups bypass the proxy.\n"
            "Please convert to a standard mongodb:// URI first (see the README)."
        )

    print("Connecting to MongoDB via QuotaGuard Shield...")
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=15000)

    result = client.admin.command("ping")
    print(f"MongoDB ping: {result}")
    print("✓ Successfully connected to MongoDB through QuotaGuard Shield")


if __name__ == "__main__":
    main()
