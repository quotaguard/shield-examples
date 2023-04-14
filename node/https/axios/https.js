const axios = require('axios');
const url = require('url');
const HttpsProxyAgent = require('https-proxy-agent');

const proxy = url.parse(process.env.QUOTAGUARDSHIELD_URL);

const proxyAgent = new HttpsProxyAgent({
  protocol: 'https:',
  host: proxy.hostname,
  port: proxy.port,
  auth: `${proxy.auth.split(':')[0]}:${proxy.auth.split(':')[1]}`
});

const fetchIp = async () => {
    try {
        const axiosInstance = axios.create({ httpsAgent: proxyAgent });

        const res = await axiosInstance.get('https://ip.quotaguard.com');
        console.log(res.data);
    } catch (err) {
        console.error(err);
    }
};

fetchIp();
