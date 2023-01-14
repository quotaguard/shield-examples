PHP HTTPS QuotaGuard Shield Example
--

# Prerequesites
This only requires curl, which generally is installed alongside php.

# Run example
```
QUOTAGUARDSTATIC_URL=... php https.php
```

Be sure to set QUOTAGUARDSHIELD_URL to your HTTP proxy URL from the [QuotaGuard Dashboard](https://www.quotaguard.com/setup/outbound).

# Test in Docker
```
docker build -t qg-shield-php-https-example .
docker run -e QUOTAGUARDSHIELD_URL=... qg-shield-php-https-example
```
