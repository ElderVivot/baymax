const axios = require('axios')
const ipSetting = require('./ip.json')

let ip = 'localhost'
try {
  ip = ipSetting.ip
} catch (error) {
  ip = 'localhost'
}

const api = axios.create({
    baseURL: `http://${ip}:3001`
})

module.exports.api = api