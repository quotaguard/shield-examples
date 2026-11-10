NodeJS Hyperliquid SDK (REST and WebSocket) QuotaGuard Shield Example
--

This example routes the [@siebly/hyperliquid-api](https://www.npmjs.com/package/@siebly/hyperliquid-api) SDK through a QuotaGuard Shield proxy using https-proxy-agent. It makes an unsigned `/info` request over REST, subscribes to the `allMids` WebSocket stream, and prints the egress IP that Hyperliquid sees. No wallet key is needed to run it.

Hyperliquid rate-limits per source IP, so a bot on a platform with rotating egress IPs trips throttles unpredictably. Routing the SDK through Shield gives every REST call and WebSocket connection the same static IP.

# Prerequisites
```
npm install @siebly/hyperliquid-api https-proxy-agent ws
```

# Run example
```
QUOTAGUARDSHIELD_URL=... node index.js
```

Be sure to set QUOTAGUARDSHIELD_URL to your HTTPS proxy URL from the [QuotaGuard Dashboard](https://www.quotaguard.com/setup/outbound).

Expected output:
```
Egress IP seen by ip.quotaguard.com: <one of your two QuotaGuard IPs>
BTC mid via REST: 73016.5
BTC mid via WebSocket: 73016.5
```

# How it works

- `RestClient` takes axios network options as its second argument. Passing `httpsAgent: new HttpsProxyAgent(QUOTAGUARDSHIELD_URL)` sends every REST call, `/info` and signed `/exchange` alike, through the proxy.
- `keepAlive: false` in the first argument is required. With the default, the SDK installs its own keep-alive agent in place of the proxy agent. Requests still succeed, but they leave from your server's own IP, so the static IP is never used. Check the printed egress IP against your dashboard rather than trusting a 200 response.
- `proxy: false` stops axios from also reading `HTTP_PROXY` / `HTTPS_PROXY` environment variables.
- `WebsocketClient` accepts a `webSocketConstructor`. The small `ProxyWebSocket` class passes the same agent to the `ws` library so the `wss://` upgrade is tunneled through the proxy too.

# Signed trading actions

Orders, cancels and transfers go to `/exchange` and must be signed. Add `privateKey` (use a Hyperliquid API wallet key, not your main wallet) to the first `RestClient` argument and the SDK signs for you. Those calls use the same proxied axios instance, so nothing else changes:

```
const client = new RestClient(
  { keepAlive: false, privateKey: process.env.HYPERLIQUID_API_WALLET_KEY },
  { httpsAgent: agent, proxy: false },
);
```

The SDK is maintained by Siebly, not QuotaGuard. See the [SDK tutorial](https://siebly.io/sdk/hyperliquid/javascript/tutorial) for its full API, including the referral and builder-code settings it applies to orders.

# Test in Docker
```
docker build -t qg-shield-node-hyperliquid-sdk-example .
docker run -e QUOTAGUARDSHIELD_URL=... qg-shield-node-hyperliquid-sdk-example
```
