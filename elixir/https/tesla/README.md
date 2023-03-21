Elixir Tesla HTTPS QuotaGuard Shield Example
--

# Prerequesites
* mix
* QGPass

# Run example
```
QUOTAGUARDSTATIC_URL=... ./bin/qgpass mix run -e "Qg.request_ip()"
```

Be sure to set QUOTAGUARDSHIELD_URL to your HTTPS proxy URL from the [QuotaGuard Dashboard](https://www.quotaguard.com/setup/outbound).

# Test in Docker
```
docker build -t qg-shield-elixir-https-tesla-example .
docker run -e QUOTAGUARDSHIELD_URL=... qg-shield-elixir-https-tesla-example
```
