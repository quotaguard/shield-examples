# QuotaGuard Shield — Python + MongoDB Example (QGTunnel)

This example shows how to connect to a MongoDB instance through a **QuotaGuard Shield**
proxy using [QGTunnel](https://devcenter.heroku.com/articles/quotaguard#qgtunnel-the-quotaguard-tunnel-client).

QGTunnel wraps your process and automatically routes all outgoing TCP connections through
the Shield proxy — no code changes to your application required.

## Requirements

```
pip install pymongo
curl https://s3.amazonaws.com/quotaguard/qgtunnel-latest.tar.gz | tar xz
```

## Environment variables

| Variable | Description |
|---|---|
| `QUOTAGUARDSHIELD_URL` | Your QuotaGuard Shield proxy URL, e.g. `https://user:password@us-east-shield-01.quotaguard.com:9294`. Found in your [QuotaGuard Dashboard](https://www.quotaguard.com/setup/outbound). |
| `MONGO_URI` | A standard `mongodb://` or `mongodb+srv://` connection string. |

## Run directly

```bash
QUOTAGUARDSHIELD_URL=https://... MONGO_URI=mongodb://... bin/qgtunnel python app.py
```

## Run in Docker

```bash
docker build -t qg-shield-python-mongo-qgtunnel-example .
docker run \
  -e QUOTAGUARDSHIELD_URL=https://... \
  -e MONGO_URI=mongodb://... \
  qg-shield-python-mongo-qgtunnel-example
```

> **Note:** `mongodb+srv://` URIs work fine here because QGTunnel intercepts DNS
> lookups as well as TCP connections.
