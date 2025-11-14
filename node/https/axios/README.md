NodeJS HTTPS Axios QuotaGuard Shield Example
--

This example utilizes axios and https-proxy-agent to make HTTPS requests through a QuotaGuard proxy.

# Prerequisites
```
npm install axios https-proxy-agent
```

# Run example
```
QUOTAGUARDSHIELD_URL=... node https.js
```

Be sure to set QUOTAGUARDSHIELD_URL to your HTTP proxy URL from the [QuotaGuard Dashboard](https://www.quotaguard.com/setup/outbound).

## Optional Parameters

- `TARGET_URL`: The endpoint to connect to (defaults to `https://ip.quotaguard.com`)
  - Must start with `http://` or `https://`
  - Supports non-standard ports (e.g., `https://example.com:8443`)

# Examples

## Default target (ip.quotaguard.com)
```
QUOTAGUARDSHIELD_URL=... node https.js
```

## Custom target with standard port
```
QUOTAGUARDSHIELD_URL=... TARGET_URL=https://httpbin.org/get node https.js
```

## Custom target with non-standard port
```
QUOTAGUARDSHIELD_URL=... TARGET_URL=https://example.com:8443 node https.js
```

# Test in Docker
```
docker build -t qg-shield-node-https-axios-example .
docker run -e QUOTAGUARDSHIELD_URL=... qg-shield-node-https-axios-example
```

## Docker with custom target
```
docker run -e QUOTAGUARDSHIELD_URL=... -e TARGET_URL=https://httpbin.org/get qg-shield-node-https-axios-example
```
