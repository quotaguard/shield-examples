Python AWS Lambda Relay QuotaGuard Shield Example
--

A small forwarding function for platforms that can make outbound HTTPS calls but cannot set a proxy (Base44, Zoho Deluge, Bubble, Zapier, and similar). Your platform calls the Lambda's URL, and the Lambda forwards the request through QuotaGuard Shield so the target sees your static IPs. The hop from the Lambda to the proxy is TLS-encrypted, and the request itself is tunneled through the proxy unchanged.

```
Your platform --> Lambda Function URL --> QuotaGuard Shield --> target API
```

Uses only libraries already present in the Lambda Python runtime, so there is nothing to package or install.

# Setup

1. In the AWS console, create a Lambda function with the **Python 3.12** runtime and paste in `lambda_function.py`.

2. Under **Configuration > Environment variables**, add:
   - `QUOTAGUARDSHIELD_URL` — your Connection URL from the [QuotaGuard Dashboard](https://www.quotaguard.com/setup/outbound). It is an `https://` URL on port 9294.
   - `RELAY_KEY` — a long random string you generate. This is the password for your relay; anyone with the URL and this key can send traffic through your proxy, so keep it secret.

3. Under **Configuration > General configuration**, set the timeout to 30 seconds (the 3-second default is tight for API calls). Raise it if the target can take longer to answer.

4. Under **Configuration > Function URL**, create a function URL with auth type **NONE**. The `RELAY_KEY` check in the code is what protects it.

# Calling the relay

Send your request to the function URL with two extra headers:

- `X-Relay-Key` — your secret key
- `X-Target-URL` — the full URL of the API you want to reach

The method, body, `Content-Type`, `Accept`, and `Authorization` headers are forwarded to the target as-is, and the target's response comes back as the relay's response. To forward any other header, prefix it with `X-Fwd-`: `X-Fwd-X-Api-Key: abc` reaches the target as `X-Api-Key: abc`.

Example with curl:

```
curl https://<your-function-url>.lambda-url.<region>.on.aws/ \
  -H "X-Relay-Key: <your secret>" \
  -H "X-Target-URL: https://ip.quotaguard.com"
```

Example from a Deno backend function (Base44 and similar):

```ts
const res = await fetch("https://<your-function-url>.lambda-url.<region>.on.aws/", {
  method: "POST",
  headers: {
    "X-Relay-Key": "<your secret>",
    "X-Target-URL": "https://api.example.com/endpoint",
    "Content-Type": "application/json",
    "Authorization": "Bearer <token>",
  },
  body: JSON.stringify(payload),
});
```

# Using one IP

Both static IPs in your dashboard are active behind the proxy hostname. If the target must see exactly one address, change the hostname in `QUOTAGUARDSHIELD_URL` from `<region>-shield-01.quotaguard.com` to `<region>-shield-01-a.quotaguard.com` (or `-b`). You keep that one fixed IP and give up automatic failover between the two.

# Test

Point `X-Target-URL` at `https://ip.quotaguard.com` (as in the curl example above). It returns the IP your request came from, which should be one of the two static IPs shown in your dashboard. Those two IPs are what you give the target API for its allowlist; both are active, so allowlist both unless you pinned one as above.
