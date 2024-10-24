Python MongoDB (pymongo) QuotaGuard Shield Example
--

# Prerequesites
```
RUN pip install --no-cache-dir pymongo
RUN curl https://s3.amazonaws.com/quotaguard/qgtunnel-latest.tar.gz | tar xz
```

# Run example
```
QUOTAGUARDSHIELD_URL=... MONGO_URI=... bin/qgtunnel python app.py
```

Be sure to set QUOTAGUARDSHIELD_URL to your proxy URL from the [QuotaGuard Dashboard](https://www.quotaguard.com/setup/outbound).

# Test in Docker
```
docker build -t qg-shield-python-mongo-pymongo-example .
docker run -e QUOTAGUARDSTATIC_URL=... -e MONGO_URI=... qg-shield-python-mongo-pymongo-example
```
