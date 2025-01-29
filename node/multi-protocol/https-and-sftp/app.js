import url from 'url';
import { HttpsProxyAgent } from 'https-proxy-agent';
import request from 'request';
import { readFile } from "fs";
import SFTPClient from 'ssh2-sftp-client';

const testEndpoint = 'https://ip.quotaguard.com';
const proxy = "http://localhost:8080"; // Corrected typo in localhost
const agent = new HttpsProxyAgent(proxy);
const options = {
  uri: url.parse(testEndpoint),
  agent
};

function callback(error, response, body) {
  if (!error && response.statusCode == 200) {
    console.log('Response from "ip.quotaguard.com": ', body);
  } else {
    console.log('error: ', error);
  }
}

request(options, callback);

agent.destroy();

const host = 'test.rebex.net';
const port = 22; // default SSH/SFTP port on remote server

const client = new SFTPClient();
client.connect({
  host,
  port,
  username: 'demo',
  password: 'password'
}).then(() => {
  console.log("Connected over SFTP, downloading readme.txt");
  return client.get("readme.txt", "readme.txt");
})
.then(() => {
  console.log("File Downloaded!");
  readFile("readme.txt", function(err, data){
    if (err) {
      console.error(err);
    } else {
      console.log(data.toString('utf8'));
    }
    client.end(); // Ensure the client exits after reading the file
    process.exit(0);
  });
})
.catch(err => {
  console.error(err.message);
  client.end(); // Ensure the client exits on error
});