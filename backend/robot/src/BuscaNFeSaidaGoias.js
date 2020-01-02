'use strict';

const puppeteer = require('puppeteer')
const fs = require('fs')
const request = require('request');

(async() => {
    const browser = await puppeteer.launch({headless: false, args: [ '--ignore-certificate-errors' ]})

    let page = await browser.newPage()

    await page.setViewport({ width:0, height:0 })
    
    await page.goto('http://nfe.sefaz.go.gov.br/nfeweb/sites/nfe/consulta-publica/principal')

    // await page.setRequestInterception(true);

    const pfx = fs.readFileSync('C:/_temp/agf_cert.pfx');
    const password = 'soma1234'
    
    await page.waitFor(3000)

    // page.on('request', interceptedRequest => {
    //     // Intercept Request, pull out request options, add in client cert
    //     const options = {
    //         uri: interceptedRequest.url(),
    //         method: interceptedRequest.method(),
    //         headers: interceptedRequest.headers(),
    //         body: interceptedRequest.postData(),
    //         pfx: pfx,
    //         passphrase: password,
    //     };

    //     // Fire off the request manually (example is using using 'request' lib)
    //     request(options, function(err, resp, body) {
    //         // Abort interceptedRequest on error
    //         if (err) {
    //             console.error(`Unable to call ${options.uri}`, err);
    //             return interceptedRequest.abort('connectionrefused');
    //         }

    //         // Return retrieved response to interceptedRequest
    //         interceptedRequest.get({
    //             status: resp.statusCode,
    //             contentType: resp.headers['content-type'],
    //             headers: resp.headers,
    //             body: body
    //         });
    //     });

    // });

    await page.click("a[href*='nfe/consulta-publica'] button")
    
    await page.waitFor(2000)
    
    // browser.close()
})()