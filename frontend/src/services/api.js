const axios = require('axios')
const prepareUrls = require('local-ip-url/prepareUrls');

const urls = prepareUrls({
  protocol: 'http',
  host: '0.0.0.0',
  port: 3001
})

const api = axios.create({
    baseURL: urls.lanUrl
})

module.exports.api = api