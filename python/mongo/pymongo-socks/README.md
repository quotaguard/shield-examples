# QuotaGuard Shield — Python + MongoDB (no QGTunnel)

Connect to MongoDB through a QuotaGuard Shield proxy using pure Python —
no QGTunnel wrapper required. Suitable for environments where you can't run a
wrapper process, such as **PythonAnywhere**.

## Using this in your own project

**1. Copy `quotaguard.py` into your project.**

**2. At the very top of your entry point — before importing `pymongo` or any other
network library — add:**

```python
from quotaguard import configure_socks_proxy
configure_socks_proxy()
```

**3. Then import and use pymongo as normal:**

```python
from pymongo import MongoClient

client = MongoClient(os.environ["MONGO_URI"])
```

That's it. Every TCP connection your process makes will be routed through the proxy.

## Requirements

```
pip install pymongo
```

## Environment variables

| Variable | Description |
|---|---|
| `QUOTAGUARDSHIELD_URL` | Your QuotaGuard Shield proxy URL: `https://user:password@us-east-shield-01.quotaguard.com:9294`. Found in your [QuotaGuard Dashboard](https://www.quotaguard.com/setup/outbound). |
| `MONGO_URI` | A standard `mongodb://` connection string with explicit hosts (see below). |

> **Note:** `mongodb+srv://` URIs are not supported — DNS SRV lookups happen before
> the proxy is involved. See below for how to convert.

## Getting a `mongodb://` URI from your `mongodb+srv://` URI

Run this once from any machine that can reach MongoDB directly:

```python
from pymongo import MongoClient

client = MongoClient("mongodb+srv://user:password@your-cluster.mongodb.net/",
                     serverSelectionTimeoutMS=10000)
info = client.admin.command("isMaster")
print("Replica Set:", info.get("setName"))
print("Hosts:", info.get("hosts"))
```

Then build your URI:

```
mongodb://user:password@host1:27017,host2:27017,host3:27017/?ssl=true&replicaSet=<setName>&authSource=admin
```

## Running the example app

```bash
# Directly
QUOTAGUARDSHIELD_URL=https://... MONGO_URI=mongodb://... python app.py

# Docker
docker build -t qg-shield-python-mongo-example .
docker run \
  -e QUOTAGUARDSHIELD_URL=https://... \
  -e MONGO_URI=mongodb://... \
  qg-shield-python-mongo-example
```
