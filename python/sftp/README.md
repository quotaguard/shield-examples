Python SFTP (paramiko) QuotaGuard Shield Static IPs Example
--

# Prerequesites
```
pip install paramiko
```

# Run example
```
QUOTAGUARDSHIELD_URL=... bin/qgtunnel python app.py
```

Be sure to set QUOTAGUARDSHIELD_URL to your Connection URL from the [QuotaGuard Dashboard](https://www.quotaguard.com/setup/outbound).

# Test in Docker
```
docker build -t qg-shield-python-sftp-paramiko-example .
docker run -e QUOTAGUARDSHIELD_URL=... qg-shield-python-sftp-paramiko-example
```
