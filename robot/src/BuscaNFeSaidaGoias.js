const puppeteer = require('puppeteer')
const fs = require('fs')
const request = require('request');

const buscaNFeSaidaGoias = async() => {
    const browser = await puppeteer.launch({headless: false, args: ['--start-maximized']})

    const page = await browser.newPage()

    await page.setViewport({ width:0, height:0 })

    // 1 - Acessa página de Goiânia
    await page.goto('http://nfe.sefaz.go.gov.br/nfeweb/sites/nfe/consulta-publica/principal')

    await page.waitFor(3000)

    // Enable Request Interception
    await page.setRequestInterception(true);

    // Client cert files
    const cert = fs.readFileSync('C:\\temp\\1\\17ac5ea3218f001e0ab18262308117b5.crt');
    const key = fs.readFileSync('C:\\temp\\1\\17ac5ea3218f001e0ab18262308117b5.key');
    console.log(cert)

    page.on('request', interceptedRequest => {
        // Intercept Request, pull out request options, add in client cert
        const options = {
            uri: interceptedRequest.url(),
            method: interceptedRequest.method(),
            headers: interceptedRequest.headers(),
            body: interceptedRequest.postData(),
            cert: cert,
            key: key
        };

        // Fire off the request manually (example is using using 'request' lib)
        request(options, function(err, resp, body) {
            // Abort interceptedRequest on error
            if (err) {
                console.error(`Unable to call ${options.uri}`, err);
                return interceptedRequest.abort('connectionrefused');
            }

            // Return retrieved response to interceptedRequest
            interceptedRequest.respond({
                status: resp.statusCode,
                contentType: resp.headers['content-type'],
                headers: resp.headers,
                body: body
            });
        });

    });

    await page.click("a[href*='nfe/consulta-publica'] button")
    
    await page.waitFor(2000)
    
    // browser.close()
}

buscaNFeSaidaGoias()