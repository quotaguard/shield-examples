FROM node:latest

WORKDIR /app/

COPY package.json /app/package.json
RUN npm install

COPY app.js /app/app.js

# Download and extract qgpass
RUN curl https://s3.amazonaws.com/quotaguard/qgpass-latest.tar.gz | tar xz -C /app/
ENV QGPASS_DEBUG true

RUN curl https://s3.amazonaws.com/quotaguard/qgtunnel-latest.tar.gz | tar xz
ENV QGTUNNEL_DEBUG true

ENTRYPOINT [ "/app/bin/qgtunnel", "/app/bin/qgpass", "node", "app.js" ]