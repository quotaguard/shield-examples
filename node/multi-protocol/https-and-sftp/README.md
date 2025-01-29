NodeJS HTTPS and SFTP using both QGTunnel and QGPass for QuotaGuard Shield Example
--

# Prerequesites
```
npm install https-proxy-agent request ssh2-sftp-client socks
curl https://s3.amazonaws.com/quotaguard/qgtunnel-latest.tar.gz | tar xz
curl https://s3.amazonaws.com/quotaguard/qgpass-latest.tar.gz | tar xz
```

# Run example
```
QUOTAGUARDSHIELD_URL=... bin/qgtunnel bin/qgpass node app.js
```

Be sure to set QUOTAGUARDSHIELD_URL to your HTTPS proxy URL from the [QuotaGuard Dashboard](https://www.quotaguard.com/setup/outbound).

# Test in Docker
```
docker build -t qg-shield-node-https-sftp-example .
docker run -e QUOTAGUARDSHIELD_URL=... qg-shield-node-https-sftp-example
```
