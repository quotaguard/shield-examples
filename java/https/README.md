Java HTTPS for QuotaGuard Shield Example
--

# Prerequesites
```

```

# Run example
```
QUOTAGUARDSHIELD_URL=... 
```

Be sure to set QUOTAGUARDSHIELD_URL to your HTTPS proxy URL from the [QuotaGuard Dashboard](https://www.quotaguard.com/setup/outbound).

# Test in Docker
```
docker build -t qg-shield-java-https-example .
docker run -e QUOTAGUARDSHIELD_URL=... qg-shield-java-https-example
```
