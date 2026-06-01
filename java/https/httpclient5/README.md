# Java HTTPS with Apache HttpClient 5 + QuotaGuard Shield

A minimal example showing how to send HTTPS requests through QuotaGuard Shield from Java using [Apache HttpClient 5](https://hc.apache.org/httpcomponents-client-5.3.x/).

## Prerequisites

- An active QuotaGuard Shield subscription. You'll need your `QUOTAGUARDSHIELD_URL` from the [dashboard](https://www.quotaguard.com/setup/outbound) — it looks like `https://username:password@us-east-shield-XX.quotaguard.com:9294`.
- Docker (the example runs in a container so you don't have to install Java locally).
- Java HTTP clients (HttpClient 5, OkHttp, HttpURLConnection, etc.) cannot dial the Shield proxy directly — see [How it works](#how-it-works) below. This example uses **QGPass**, a small helper we ship that bridges the gap.

## Build and run

```bash
docker build -t qg-shield-httpclient5-example .
docker run --rm \
  -e QUOTAGUARDSHIELD_URL='https://username:password@us-east-shield-XX.quotaguard.com:9294' \
  qg-shield-httpclient5-example
```

Expected output:

```
Response code: 200
{"ip":"<one of your Shield static IPs>"}
```

The example calls `https://ip.quotaguard.com`, which echoes the egress IP of the request. If you see a 200 and an IP from your subscription, the integration is working.

## How it works

QuotaGuard Shield's outbound HTTPS proxy listens on port 9294 with **TLS wrapping the proxy connection itself**. That is, the connection from your application to the proxy is encrypted, and the credentials are transmitted inside that TLS tunnel. Standard Java HTTP clients (HttpClient 5 included) do not natively dial a proxy over TLS — they expect to open a plain TCP connection to the proxy and then optionally `CONNECT` to an HTTPS destination.

To bridge that, we ship **QGPass**. QGPass runs alongside your Java process, listens on `http://localhost:8080`, reads `QUOTAGUARDSHIELD_URL` from the environment, and handles the TLS hop plus Basic auth. Your Java code only needs to know about `localhost:8080` as a plain HTTP proxy — no credentials in the source, no TLS configuration.

The Dockerfile fetches QGPass from S3 and launches the JVM under it:

```dockerfile
RUN curl -sSL https://s3.amazonaws.com/quotaguard/qgpass-latest.tar.gz | tar xz -C /app/
# ...
CMD ["bin/qgpass", "java", "HttpsTest"]
```

For HTTPS destinations, your client sends a `CONNECT host:443` to QGPass, which forwards it through the Shield proxy, and your TLS handshake terminates between your app and the destination server. QuotaGuard never sees the plaintext payload.

## The code

See [HttpsTest.java](HttpsTest.java). The HttpClient 5-specific configuration is one line:

```java
HttpHost proxy = new HttpHost("http", "localhost", 8080);

CloseableHttpClient client = HttpClients.custom()
        .setProxy(proxy)
        .build();
```

That's the whole integration. The `HttpHost` scheme is `"http"` (the local hop to QGPass is plain HTTP) and it points at `localhost:8080`.

### Gradle dependency

```groovy
dependencies {
    implementation 'org.apache.httpcomponents.client5:httpclient5:5.3.1'
}
```

No QuotaGuard-specific library is needed — QGPass runs as a separate process, not a Java dependency.

## Troubleshooting

- **Connection timeout / hang** — most often this means QGPass isn't running. Confirm your `CMD` launches the JVM via `bin/qgpass`, not bare `java`.
- **`407 Proxy Authentication Required`** — usually means you're pointing HttpClient directly at the `*.quotaguard.com:9294` URL instead of at QGPass. Java HTTP clients can't authenticate to the Shield proxy directly; let QGPass handle it.
- **Anything else** — non-`407` HTTP status codes come from your destination server, not from QuotaGuard.

## See also

- [HttpURLConnection example](../httpurlconnection/) — same idea using Java's built-in client
- [OkHttp example](../okhttp/) — same idea using OkHttp
