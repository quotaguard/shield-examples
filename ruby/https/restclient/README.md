Ruby HTTPS w/ RestClient QuotaGuard Shield Example
--

# Run example
```
QUOTAGUARDSHIELD_URL=... bin/qgpass ruby restclient.rb
```

Be sure to set QUOTAGUARDSHIELD_URL to your Connection URL from the [QuotaGuard Dashboard](https://www.quotaguard.com/setup/outbound).

# Test in Docker
```
docker build -t qg-shield-ruby-restclient-example .
docker run -e QUOTAGUARDSHIELD_URL=... qg-shield-ruby-restclient-example
```
