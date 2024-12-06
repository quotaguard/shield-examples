const axios = require('axios');
const { HttpsProxyAgent } = require('https-proxy-agent');

const proxyUrl = process.env.QUOTAGUARDSHIELD_URL;

const fetchIp = async () => {
    try {
        // Create an HTTPS agent that tunnels through the proxy
        const httpsAgent = new HttpsProxyAgent(proxyUrl);

        const axiosInstance = axios.create({
            httpsAgent
        });

        const res = await axiosInstance.get('https://ip.quotaguard.com');
        console.log(res.data);
    } catch (err) {
        console.error(err);
    }
};

fetchIp();
