const axios = require('axios');
const url = require('url');

const proxy = url.parse(process.env.QUOTAGUARDSHIELD_URL);
const auth = proxy.auth.split(':');

const fetchIp = async () => {
    try {
        const axiosInstance = axios.create({
            proxy: {
                protocol: 'https',
                host: proxy.hostname,
                port: proxy.port,
                auth: {
                    username: auth[0],
                    password: auth[1]
                }
            }
        });

        const res = await axiosInstance.get('https://ip.quotaguard.com');
        console.log(res.data);
    } catch (err) {
        console.error(err);
    }
};

fetchIp();