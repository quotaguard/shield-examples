Python Google Cloud Run Functions Relay QuotaGuard Shield Example
--

A small forwarding function for platforms that can make outbound HTTP calls but cannot set a proxy (Google Apps Script, Zoho Deluge, Bubble, Zapier, Base44, and similar). Your platform calls the function's URL, and the function forwards the request through QuotaGuard Shield so the target API sees your static IPs. The hop from the function to the proxy is TLS-encrypted, and the request itself is tunneled through the proxy unchanged.

```
Your platform --> Cloud Run function URL --> QuotaGuard Shield --> target API
```

This is the Google Cloud counterpart of the [AWS Lambda relay](../lambda-relay). Same inputs, same headers, same behaviour. Cloud Run hands the function a Flask request object instead of Lambda's event dictionary, which is the only reason the two files differ.

# Setup

Google now deploys Cloud Functions as Cloud Run functions, so the steps below use the Cloud Run page of the console.

1. In the Google Cloud console, open **Cloud Run** and click **Write a function**. Give the service a name, pick the region closest to your QuotaGuard region, and choose the **Python 3.12** runtime.

2. Under **Authentication**, select **Allow public access**. The `RELAY_KEY` check in the code is what protects the function.

3. Under **Variables & Secrets** (in the Containers section), add:
   - `QUOTAGUARDSHIELD_URL` — your Connection URL from the [QuotaGuard Dashboard](https://www.quotaguard.com/setup/outbound). It is an `https://` URL on port 9294.
   - `RELAY_KEY` — a long random string you generate. This is the password for your relay; anyone with the URL and this key can send traffic through your proxy, so keep it secret.

4. Click **Create**. In the **Source** tab, paste `main.py` and `requirements.txt` into their tabs, set **Function entry point** to `relay`, and click **Save and redeploy**. The service URL shown at the top of the page is what your platform calls.

The function gives the target 30 seconds to answer. If the target can take longer, raise the `timeout` in `main.py` and the service's request timeout together.

Opening the service URL in a browser should return `Forbidden`. That means the function is up and the key check is working.

# Calling the relay

Send your request to the service URL with two extra headers:

- `X-Relay-Key` — your secret key
- `X-Target-URL` — the full URL of the API you want to reach

The method, body, `Content-Type`, `Accept`, and `Authorization` headers are forwarded to the target as-is, and the target's response comes back as the relay's response. To forward any other header, prefix it with `X-Fwd-`: `X-Fwd-X-Api-Key: abc` reaches the target as `X-Api-Key: abc`.

Example with curl:

```
curl https://<your-service-url>.run.app/ \
  -H "X-Relay-Key: <your secret>" \
  -H "X-Target-URL: https://ip.quotaguard.com"
```

Example from Google Apps Script, with the URL and key stored in Script Properties:

```javascript
function callThroughRelay() {
  var props = PropertiesService.getScriptProperties();
  var response = UrlFetchApp.fetch(props.getProperty('RELAY_URL'), {
    method: 'post',
    contentType: 'application/json',
    headers: {
      'X-Relay-Key': props.getProperty('RELAY_KEY'),
      'X-Target-URL': 'https://api.example.com/endpoint'
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  });
  Logger.log(response.getContentText());
}
```

# Using one IP

Both static IPs in your dashboard are active behind the proxy hostname. If the target must see exactly one address, change the hostname in `QUOTAGUARDSHIELD_URL` from `<region>-shield-01.quotaguard.com` to `<region>-shield-01-a.quotaguard.com` (or `-b`). You keep that one fixed IP and give up automatic failover between the two.

# Test

Point `X-Target-URL` at `https://ip.quotaguard.com` (as in the curl example above). It returns the IP your request came from, which should be one of the two static IPs shown in your dashboard. Those two IPs are what you give the target API for its allowlist; both are active, so allowlist both unless you pinned one as above.
