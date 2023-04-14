FROM node:latest

COPY https.js /app/https.js

WORKDIR /app/

RUN npm install axios

ENTRYPOINT [ "node", "https.js" ]
