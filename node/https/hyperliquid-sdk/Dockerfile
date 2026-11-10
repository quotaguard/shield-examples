FROM node:22-alpine

COPY index.js /app/index.js

WORKDIR /app/

RUN npm install --no-audit --no-fund @siebly/hyperliquid-api https-proxy-agent ws

ENTRYPOINT [ "node", "index.js" ]
