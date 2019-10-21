const puppeteer = require('puppeteer')
const fs = require('fs')

const buscaNFSeGoiania = async() => {
    const browser = await puppeteer.launch({headless: false, args: ['--start-maximized']})

    const page = await browser.newPage()

    await page.setViewport({ width:0, height:0 })

    // 1 - Acessa página de Goiânia
    await page.goto('https://www10.goiania.go.gov.br/Internet/Login.aspx')
    
    // 2 - Faz loguin
    await page.type('#wt38_wtLoginContent_wtUserNameInput', '02319085122')
    await page.type('#wt38_wtLoginContent_wtPasswordInput', '3771814')
    await page.click('#wt38_wtLoginContent_wt8')

    await page.waitFor(1000)

    // 3 - Clica no botão portal do contribuinte
    await page.click('#GoianiaTheme_wt27_block_wtMainContent_wtSistemaTable_ctl03_wt28')

    await page.waitFor(3000)

    // 4 - clicando no botão Nota Fiscal
    await page.click('#GoianiaTheme_wtTelaPrincipal_block_wtMainContent_wt25_WebPatterns_wt72_block_wtText_wtNFEletronica')

    await page.waitFor(3000)

    // 5 - Abre a página da Nota Fiscal e passa pelo alert
    try {
        const linkOpenPageDown = await page.evaluate( 
            () => document.querySelector('#GoianiaTheme_wtTelaPrincipal_block_wtMainContent_wt25_WebPatterns_wt50_block_wtContent_wt229').getAttribute('href')
        );
        console.log(linkOpenPageDown)
        // o then é pra passar pelo alert
        await page.goto(linkOpenPageDown).then(
            await page.on('dialog', async dialog => {
                await dialog.accept()
            })
        )
    } catch (e) {
        console.log(e)
    }

    await page.waitFor(3000)

    // 6 - Passa pelo Alerta do Simples Nacional que Abre
    const frameAlertSimplesNacional = page.frames().find(frame => frame.name() === 'cpo');
    await frameAlertSimplesNacional.click('center a')
    
    await page.waitFor(3000)

    // 7 - Clica no botão de Download do XML
    const frameDownXML = page.frames().find(frame => frame.name() === 'cpo');
    await frameDownXML.click("tr td font a[href*='snfse00200f3']")

    // // INICIO --> Esta é a forma antiga que eu fazia pra clicar no texto Download de XML de Notas Fiscais por período, as duas linhas acima resolveram isto
    // // PRIMEIRO pega a altura entre o início da página e o frame
    // const heightHeaderDownXML = await page.evaluate( () => {
    //     // função que pega a altura
    //     function offset(el) {
    //         let rect = el.getBoundingClientRect(),
    //         scrollLeft = window.pageXOffset || document.documentElement.scrollLeft,
    //         scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    //         return { top: rect.top + scrollTop, left: rect.left + scrollLeft }
    //     }

    //     let elementSelected = document.querySelector('[name=cpo]');
    //     let elementSelectedOffset = offset(elementSelected);
    //     return elementSelectedOffset.top
    // })

    // // SEGUNDO - Pega altura do objeto agora, que no caso é o Download de XML de Notas Fiscais
    // const aHandleDownXML = await frameDownXML.evaluateHandle(() => document.body);
    // const resultHandleDownXML = await frameDownXML.evaluateHandle(body => body.innerHTML, aHandleDownXML);
    // const positionDownXML = await resultHandleDownXML.evaluate( () => {
    //     function offset(el) {
    //         let rect = el.getBoundingClientRect(),
    //         scrollLeft = window.pageXOffset || document.documentElement.scrollLeft,
    //         scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    //         return { top: rect.top + scrollTop, left: rect.left + scrollLeft }
    //     }
    //     // Vai percorrer todos os elementos, até encontrar aquele que quero
    //     let options = Array.from(document.querySelectorAll("tr td font b"));
    //     let optionSelected = options.filter(option => option.textContent == "Download de XML de Notas Fiscais por período")
    //     let elementSelectedOffset = offset(optionSelected[0]);
    //     return [elementSelectedOffset.left, elementSelectedOffset.top]
    // })
    // // CLICA no local que precisa, lembrando que altura é necessário somar o cabeçalho
    // await page.mouse.click(positionDownXML[0], positionDownXML[1]+heightHeaderDownXML)

    await page.waitFor(3000)

    // 8 - Seleciona o Período
    const frameSelectedPeriod = page.frames().find(frame => frame.name() === 'cpo');
    await frameSelectedPeriod.select('[name=txt_dia_inicial]', "01");
    // esta promise é pra quando o botão Listar abrir numa nova aba ela possa fechar e voltar pra aba principal com o conteúdo através 
    // da linha page.goto(popup.url())
    const newPagePromise = new Promise(x => browser.once('targetcreated', target => x(target.page())));	
    await frameSelectedPeriod.click('[value=Listar]')
    const popup = await newPagePromise;
    await page.goto(popup.url())
    
    // 9 - Abre o conteúdo do texto (xml) em nova aba
    page.click('a[href')

    await page.waitFor(3000)

    // 10 - Pega o conteúdo do texto (xml) pra salvar xml
    const notasFiscais = await page.evaluate( 
        () => document.querySelector("body pre").textContent
    )

    // 11 - Salva o XML
    fs.writeFile('notas.xml', `<geral>${notasFiscais}</geral>`, (err) => { 
        if (err) throw err;
    })
    
    await page.waitFor(2000)
    
    browser.close()
}

buscaNFSeGoiania()