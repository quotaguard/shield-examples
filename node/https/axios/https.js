const axios = require('axios');
const { HttpsProxyAgent } = require('https-proxy-agent');

const proxyUrl = process.env.QUOTAGUARDSHIELD_URL;

// HTTPS endpoint for the proxy to connect to
const endpoint = process.env.TARGET_URL || 'https://ip.quotaguard.com';

// Validate endpoint format
if (!endpoint.startsWith('https://') && !endpoint.startsWith('http://')) {
  console.error('Error: TARGET_URL must start with "http://" or "https://"');
  console.error('Current value:', endpoint);
  process.exit(1);
}

const fetchIp = async () => {
    try {
        // Create an HTTPS agent that tunnels through the proxy
        const httpsAgent = new HttpsProxyAgent(proxyUrl);

        const axiosInstance = axios.create({
            httpsAgent
        });

        const res = await axiosInstance.get(endpoint);
        console.log('Status Code:', res.status);
        console.log('Response headers:', res.headers);
        console.log(res.data);
    } catch (err) {
        console.error('Error:', err.message);
        if (err.response) {
            console.error('Status Code:', err.response.status);
            console.error('Response headers:', err.response.headers);
        }
    }
};

fetchIp();
