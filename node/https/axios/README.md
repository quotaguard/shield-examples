NodeJS HTTPS Axios QuotaGuard Shield Example
--

# Prerequesites
```
npm install axios
```

# Run example
```
QUOTAGUARDSHIELD_URL=... node https.js
```

Be sure to set QUOTAGUARDSHIELD_URL to your HTTP proxy URL from the [QuotaGuard Dashboard](https://www.quotaguard.com/setup/outbound).

# Test in Docker
```
docker build -t qg-shield-node-https-axios-example .
docker run -e QUOTAGUARDSHIELD_URL=... qg-shield-node-https-axios-example
```
