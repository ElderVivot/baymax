const axios = require('axios')

const api = axios.create({
    baseURL: 'http://192.168.254.227:3001'
})

module.exports.api = api