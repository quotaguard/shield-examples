# Java HTTPS HttpURLConnection Example for QuotaGuard Shield

This example demonstrates the original approach using Java's built-in `HttpURLConnection` with QuotaGuard Shield through QGPass.

## How it Works

This example uses Java's standard `HttpURLConnection` with system proxy properties. It **requires QGPass** because `HttpURLConnection` doesn't handle proxy authentication as elegantly as OkHttp.

## Build and Run

```bash
docker build -t qg-shield-httpurlconnection-example .
docker run -e QUOTAGUARDSHIELD_URL=https://username:password@your-proxy.quotaguard.com:9294 qg-shield-httpurlconnection-example
```

## Why QGPass is Required

`HttpURLConnection` uses system properties for proxy configuration:
- `https.proxyHost=localhost`
- `https.proxyPort=8080`

It doesn't handle proxy authentication headers as cleanly as OkHttp, so QGPass acts as a local proxy that handles the authentication to QuotaGuard Shield.

Be sure to set `QUOTAGUARDSHIELD_URL` to your HTTPS proxy URL from the [QuotaGuard Dashboard](https://www.quotaguard.com/setup/outbound).
