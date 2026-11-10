NodeJS Hyperliquid SDK (axios and ws) through QuotaGuard Shield Example
--

This example shows how to route a third-party Node.js SDK built on axios and ws through a QuotaGuard Shield proxy, using [@siebly/hyperliquid-api](https://www.npmjs.com/package/@siebly/hyperliquid-api) as the concrete case. It makes an unsigned `/info` request over REST, subscribes to the `allMids` WebSocket stream, and prints the egress IP so you can confirm the static IP is in use. No wallet key is needed to run it.

The same pattern applies to any SDK that lets you pass axios network options and a custom WebSocket constructor.

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
- `keepAlive: false` in the first argument is required. With the default, the SDK installs its own keep-alive agent in place of the proxy agent. Requests still succeed, but they leave from your server's own IP, so the static IP is never used. Check the printed egress IP against your dashboard rather than trusting a 200 response. Other SDKs can do the same thing, so verify the egress IP whichever library you use.
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

# Test in Docker
```
docker build -t qg-shield-node-hyperliquid-sdk-example .
docker run -e QUOTAGUARDSHIELD_URL=... qg-shield-node-hyperliquid-sdk-example
```
