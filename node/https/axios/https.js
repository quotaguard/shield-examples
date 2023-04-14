const axios = require('axios');
const url = require('url');

const proxy = url.parse(process.env.QUOTAGUARDSHIELD_URL);

const fetchIp = async () => {
    try {
        const res = await axios.get('https://ip.quotaguard.com',{
          proxy: {
            host: proxy.hostname,
            port: proxy.port,
            auth: {
              username: proxy.auth.split(':')[0],
              password: proxy.auth.split(':')[1]
            }
          }
        });
        console.log(res.data);
    } catch (err) {
        console.error(err);
    }
};

fetchIp();
