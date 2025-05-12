Python HTTPS w/ HTTPx QuotaGuard Shield Example
--

# Run example
```
QUOTAGUARDSHIELD_URL=... python app.py
```

Be sure to set QUOTAGUARDSHIELD_URL to your Connection URL from the [QuotaGuard Dashboard](https://www.quotaguard.com/setup/outbound).

# Test in Docker
```
docker build -t qg-shield-python-https-httpx-example .
docker run -e QUOTAGUARDSHIELD_URL=... qg-shield-python-https-httpx-example
```
