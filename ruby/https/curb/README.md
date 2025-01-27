Ruby HTTPS w/ Curb QuotaGuard Shield Example
--

# Run example
```
QUOTAGUARDSHIELD_URL=... ruby net-http.rb
```

Be sure to set QUOTAGUARDSHIELD_URL to your Connection URL from the [QuotaGuard Dashboard](https://www.quotaguard.com/setup/outbound).

# Test in Docker
```
docker build -t qg-shield-ruby-curb-example .
docker run -e QUOTAGUARDSHIELD_URL=... qg-shield-ruby-curb-example
```
