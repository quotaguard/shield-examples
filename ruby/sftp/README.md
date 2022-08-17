Ruby SFTP QuotaGuard Shield Example
--

# Prerequesites
```bash
# QGTunnel
curl https://s3.amazonaws.com/quotaguard/qgtunnel-latest.tar.gz | tar xz

# SFTP Gem
gem install net-sftp
```

# Run example
```
QUOTAGUARDSHIELD_URL=... ./bin/qgtunnel ruby sftp.rb
```

Be sure to set QUOTAGUARDSHIELD_URL to your Connection URL from the [QuotaGuard Dashboard](https://www.quotaguard.com/setup/outbound).

# Test in Docker
```
docker build -t qg-shield-ruby-sftp-example .
docker run -e QUOTAGUARDSHIELD_URL=... qg-shield-ruby-sftp-example
```
