'use strict';

const puppeteer = require('puppeteer-extra')
const fs = require('fs')
const request = require('request')
const https = require('https')
const axios = require('axios')
const path = require('path')
const RecaptchaPlugin = require('puppeteer-extra-plugin-recaptcha');

const MainNFGoias = async() => {
    
    puppeteer.use(
        RecaptchaPlugin({
            provider: {
            id: '2captcha',
            token: 'f5bbbe0d9b28601425ee0b316e391540' // REPLACE THIS WITH YOUR OWN 2CAPTCHA API KEY ⚡
            },
            visualFeedback: true // colorize reCAPTCHAs (violet = detected, green = solved)
        })
    )

    const browser = await puppeteer.launch({
        headless: false, args: ['--start-maximized'],
        executablePath: path.join('C:', 'Program Files (x86)', 'Google', 'Chrome', 'Application', 'chrome.exe')
    })

    let page = await browser.newPage()

    await page.setViewport({ width:0, height:0 })        
    
    const pfx = fs.readFileSync('C:/_temp/certificados/alr_eletrica.pfx')
    const password = '1062reis'

    await page.setRequestInterception(true)
    page.on('request', interceptedRequest => {
        // request({
        //     uri: interceptedRequest.url(),
        //     method: interceptedRequest.method(),
        //     // headers: interceptedRequest.headers(),
        //     // body: interceptedRequest.postData(),
        //     rejectUnauthorized: false,
        //     // strictSSL: true,
        //     pfx: pfx,
        //     passphrase: password,
        //     gzip: true
        // }, (function(err, resp, body) {
        //     console.log(err)
        //     if (interceptedRequest.url().endsWith('.ico')){
        //         return
        //     }
        //     console.log(resp)

        //     return interceptedRequest.respond({
        //         status: resp.statusCode,
        //         contentType: resp.headers['content-type'],
        //         headers: resp.headers,
        //         body: body
        //     });
        // }))

        // axios.request({
        //     baseURL: 'https://nfe.sefaz.go.gov.br',
        //     method: interceptedRequest.method(),
        //     headers: interceptedRequest.headers(),
            
        //     httpsAgent: new https.Agent({
        //         passphrase: password,
        //         pfx: pfx
        //     })
        // })
        // .then(resp => {
        //     console.log(resp)
            
        // })
        // .catch(error => console.error(error));

        https.request({
            servername: 'https://nfe.sefaz.go.gov.br',
            href: 'https://nfe.sefaz.go.gov.br',
            pfx: pfx,
            passphrase: password
        })
        
    });
    
    await page.goto('https://nfe.sefaz.go.gov.br/nfeweb/sites/nfe/consulta-publica/principal')

    await page.waitFor(3000)

    await page.click("a[href*='nfe.sefaz.go.gov'] > button")

    await page.waitFor(3000)

    await page.solveRecaptchas()

    await page.click("button[form='filtro']")

    await page.waitFor(5000)

    await page.click(".btn-download-all")

    await page.waitFor(3000)

    await page.click('#dnwld-all-btn-ok')
    
    await page.waitFor(3000)
    
    // await browser.close()
}

MainNFGoias()