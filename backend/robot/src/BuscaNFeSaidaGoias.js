'use strict';

const puppeteer = require('puppeteer')
const fs = require('fs')
const request = require('request')
const path = require('path')

const MainNFGoias = async() => {
    const browser = await puppeteer.launch({
        headless: false, ignoreHTTPSErrors: true, args: [ '--ignore-certificate-errors' ],
        executablePath: path.join('C:', 'Program Files (x86)', 'Google', 'Chrome', 'Application', 'chrome.exe')
    })

    let page = await browser.newPage()

    await page.setViewport({ width:0, height:0 })        
    
    const pfx = fs.readFileSync('C:/_temp/certificados/alr_eletrica.pfx');
    const password = '1062reis'
    
    await page.goto('http://nfe.sefaz.go.gov.br/nfeweb/sites/nfe/consulta-publica/principal').then(
        
    )

    await page.waitFor(3000)
    
    await page.click("a[href*='nfe/consulta-publica'] button").then(
        await page.setRequestInterception(true),
        page.on('request', interceptedRequest => {
            // Intercept Request, pull out request options, add in client cert
            const options = {
                uri: interceptedRequest.url(),
                method: interceptedRequest.method(),
                headers: interceptedRequest.headers(),
                body: interceptedRequest.postData(),
                rejectUnauthorized: false,
                agentOptions: {
                    pfx: pfx,
                    passphrase: password
                }
            }
            
            // Fire off the request manually (example is using using 'request' lib)
            request(options, function(err, resp, body) {
                if (interceptedRequest.url().endsWith('.ico')){
                    return
                }

                // Abort interceptedRequest on error
                if (err) {
                    console.error(`Unable to call ${options.uri}`, err);
                    return interceptedRequest.abort('connectionrefused');
                }
    
                // Return retrieved response to interceptedRequest
                return interceptedRequest.respond({
                    status: resp.statusCode,
                    contentType: resp.headers['content-type'],
                    headers: resp.headers,
                    body: body
                })
            })
        })
    )

    await page.waitFor(2000)

    // await page.click("a[href*='nfe/consulta-publica'] button")
    
    // browser.close()
}

MainNFGoias()