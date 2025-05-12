import os
import httpx

QUOTAGUARD_URL = os.getenv("QUOTAGUARDSHIELD_URL", "")
TEST_URL = "https://ip.quotaguard.com/"

if not QUOTAGUARD_URL:
    print("Error: QUOTAGUARD_URL environment variable not set.")
    exit(1)

try:
    response = httpx.get(TEST_URL, proxy=QUOTAGUARD_URL)
    print("Response from QuotaGuard:")
    print(response.text)
except Exception as e:
    print("Request failed:")
    print(e)
