FROM node:latest

COPY https.js /app/https.js

WORKDIR /app/

RUN npm install https-proxy-agent request

ENTRYPOINT [ "node", "https.js" ]
