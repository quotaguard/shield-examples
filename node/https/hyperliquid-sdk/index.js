const { HttpsProxyAgent } = require('https-proxy-agent');
const { RestClient, WebsocketClient, DefaultLogger } = require('@siebly/hyperliquid-api');
const WebSocket = require('ws');

const proxyUrl = process.env.QUOTAGUARDSHIELD_URL;
if (!proxyUrl) {
  console.error('Error: set QUOTAGUARDSHIELD_URL to your Shield proxy URL from the QuotaGuard dashboard');
  process.exit(1);
}

// One agent carries both the REST calls and the WebSocket upgrade through the proxy.
const agent = new HttpsProxyAgent(proxyUrl);

// keepAlive: false is required. When keepAlive is left at its default the SDK
// installs its own keep-alive https.Agent in place of this one, the requests
// still succeed, and they leave from your server's own IP instead of the proxy.
// proxy: false stops axios from also reading HTTP_PROXY / HTTPS_PROXY.
const client = new RestClient(
  { keepAlive: false },
  { httpsAgent: agent, proxy: false },
);

// The SDK accepts a custom WebSocket constructor. This one passes the proxy
// agent to ws so the wss:// connection is tunneled through the same static IP.
class ProxyWebSocket {
  constructor(url) {
    return new WebSocket(url, { agent });
  }
}

const main = async () => {
  // 1. Prove the egress IP. This is the same axios instance the SDK uses.
  const ip = await client.axios.get('https://ip.quotaguard.com');
  console.log('Egress IP seen by ip.quotaguard.com:', ip.data.ip);

  // 2. Unsigned /info request through the proxy. No wallet key needed.
  const mids = await client.getAllMids();
  console.log('BTC mid via REST:', mids.BTC);

  // 3. WebSocket subscription through the proxy. Exit after the first message.
  // The SDK logs connection events to the console by default. Keep errors, drop info.
  const quietLogger = { ...DefaultLogger, info: () => {} };
  const ws = new WebsocketClient(
    {
      webSocketConstructor: ProxyWebSocket,
      keepAlive: false,
      requestOptions: { httpsAgent: agent, proxy: false },
    },
    quietLogger,
  );

  await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('No WebSocket message within 20s')), 20000);
    ws.on('message', (msg) => {
      console.log('BTC mid via WebSocket:', msg.data && msg.data.mids && msg.data.mids.BTC);
      clearTimeout(timer);
      resolve();
    });
    ws.on('exception', (e) => {
      clearTimeout(timer);
      reject(e.event || e);
    });
    ws.subscribe({ type: 'allMids' }).catch(reject);
  });

  ws.closeAll();
};

main()
  .then(() => process.exit(0))
  .catch((err) => {
    console.error('Error:', err && err.message ? err.message : err);
    process.exit(1);
  });
