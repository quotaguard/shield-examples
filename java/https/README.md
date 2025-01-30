Java HTTPS for QuotaGuard Shield Example
--

# Prerequesites
```
curl -sSL https://s3.amazonaws.com/quotaguard/qgpass-latest.tar.gz
```

# Run example
```
javac HttpsTest.java
QUOTAGUARDSHIELD_URL=... bin/qgpass java HttpsTest
```

Be sure to set QUOTAGUARDSHIELD_URL to your HTTPS proxy URL from the [QuotaGuard Dashboard](https://www.quotaguard.com/setup/outbound).

# Test in Docker
```
docker build -t qg-shield-java-https-example .
docker run -e QUOTAGUARDSHIELD_URL=... qg-shield-java-https-example
```
