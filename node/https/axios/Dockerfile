FROM node:latest

COPY https.js /app/https.js

WORKDIR /app/

RUN npm install axios https-proxy-agent

ENTRYPOINT [ "node", "https.js" ]
