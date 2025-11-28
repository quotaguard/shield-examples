# Java HTTPS OkHttp Example for QuotaGuard Shield

This example demonstrates how to use OkHttp with QuotaGuard Shield proxy through QGPass.

## Build and Run

```bash
docker build -t qg-shield-okhttp-example .
docker run -e QUOTAGUARDSHIELD_URL=https://username:password@your-proxy.quotaguard.com:9294 qg-shield-okhttp-example
```

## How it Works

The application connects to QGPass (localhost:8080) which handles authentication and tunneling to the actual QuotaGuard Shield proxy. QGPass is required because QuotaGuard Shield proxies don't accept direct HTTPS tunnel connections from client applications.

Be sure to set `QUOTAGUARDSHIELD_URL` to your HTTPS proxy URL from the [QuotaGuard Dashboard](https://www.quotaguard.com/setup/outbound).
