const axios = require('axios')
require('dotenv/config')

const api = axios.create({
    baseURL: `http://192.168.254.101:3001`
})

module.exports.api = api