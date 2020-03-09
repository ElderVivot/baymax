const puppeteer = require('puppeteer')
const fs = require('fs')

const searchNFSeGoiania = async(loguin='02319085122', password='3771814') => {
    const browser = await puppeteer.launch({headless: false, args: ['--start-maximized']})
    const page = await browser.newPage()
    await page.setViewport({ width:0, height:0 })

    const checkIfLoadedThePage = async(selector, isAFrame=false, pageToSearch='') => {
        if(pageToSearch === ""){
            pageToSearch = page
        } else {
            pageToSearch = pageToSearch
        }

        const searchSelectorAlreadyExists = async(timeout=0) => {
            await pageToSearch.waitFor(timeout*1000)
            result = false
            try {
                if(isAFrame === false){
                    const fieldIsValid = await pageToSearch.evaluate( selectorFilter => document.querySelector(selectorFilter), selector )
                    if(fieldIsValid !== null){
                        result = true
                    } else {
                        result = false
                    }
                } else {
                    const fieldIsValid = pageToSearch.frames().find(frame => frame.name() === selector);
                    if(fieldIsValid !== null){
                        result = true
                    } else {
                        result = false
                    }
                }
            } catch (error) {
                result = false
            }
            return result
        }
        
        let countTry = 1
        let resultSearchSelector = await searchSelectorAlreadyExists()
        while(resultSearchSelector === false) {
            countTry += 1
            resultSearchSelector = await searchSelectorAlreadyExists(timeout=countTry)
        }
        return true
    }

    // 1 - Acessa página de Goiânia
    await page.goto('https://www10.goiania.go.gov.br/Internet/Login.aspx')
    
    // 2 - Faz loguin
    await checkIfLoadedThePage('#wt38_wtLoginContent_wtUserNameInput')
    await page.type('#wt38_wtLoginContent_wtUserNameInput', loguin)
    await page.type('#wt38_wtLoginContent_wtPasswordInput', password)
    await page.click('#wt38_wtLoginContent_wt8')
    
    // 3 - Clica no botão portal do contribuinte
    await checkIfLoadedThePage('#GoianiaTheme_wt27_block_wtMainContent_wtSistemaTable_ctl03_wt28')
    await page.click('#GoianiaTheme_wt27_block_wtMainContent_wtSistemaTable_ctl03_wt28')
    
    // 4 - clicando no botão Nota Fiscal
    await checkIfLoadedThePage('#GoianiaTheme_wtTelaPrincipal_block_wtMainContent_WebPatterns_wt157_block_wtContent1_wt54_WebPatterns_wt370_block_wtContent_WebPatterns_wt477_block_wtText_wtNFEletronica')
    await page.click('#GoianiaTheme_wtTelaPrincipal_block_wtMainContent_WebPatterns_wt157_block_wtContent1_wt54_WebPatterns_wt370_block_wtContent_WebPatterns_wt477_block_wtText_wtNFEletronica', {waitUntil: 'domcontentloaded'})
     
    // 5 - Abre a página da Nota Fiscal e passa pelo alert
    await checkIfLoadedThePage('#GoianiaTheme_wtTelaPrincipal_block_wtMainContent_WebPatterns_wt157_block_wtContent1_wt54_WebPatterns_wt70_block_wtContent_wt298')
    try {
        const linkOpenPageDown = await page.evaluate( 
            () => document.querySelector('#GoianiaTheme_wtTelaPrincipal_block_wtMainContent_WebPatterns_wt157_block_wtContent1_wt54_WebPatterns_wt70_block_wtContent_wt298').getAttribute('href')
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

    await page.screenshot({
        path: 'C:/programming/baymax/backend/robot/data/temp/teste1.png'
    });

    // await page.waitFor(7000)

    // 6 - Passa pelo Alerta do Simples Nacional que Abre
    await checkIfLoadedThePage('cpo', isAFrame=true)
    const frameAlertSimplesNacional = page.frames().find(frame => frame.name() === 'cpo');
    await checkIfLoadedThePage('center a', isAFrame=false, frameAlertSimplesNacional)
    await frameAlertSimplesNacional.click('center a')
    
    // await page.waitFor(5000)

    // 7 - Clica no botão de Download do XML
    await checkIfLoadedThePage('cpo', isAFrame=true)
    const frameDownXML = page.frames().find(frame => frame.name() === 'cpo');
    await checkIfLoadedThePage("tr td font a[href*='snfse00200f3']", isAFrame=false, frameDownXML)
    await frameDownXML.click("tr td font a[href*='snfse00200f3']")

    await page.waitFor(3000)

    // 8 - Seleciona o Período
    await checkIfLoadedThePage('cpo', isAFrame=true)
    const frameSelectedPeriod = page.frames().find(frame => frame.name() === 'cpo');
    await checkIfLoadedThePage('[name=txt_dia_inicial]', isAFrame=false, frameSelectedPeriod)
    await frameSelectedPeriod.select('[name=txt_dia_inicial]', "01");
    // esta promise é pra quando o botão Listar abrir numa nova aba ela possa fechar e voltar pra aba principal com o conteúdo através 
    // da linha page.goto(popup.url())
    const newPagePromise = new Promise(x => browser.once('targetcreated', target => x(target.page())));	
    await checkIfLoadedThePage('[value=Listar]', isAFrame=false, frameSelectedPeriod)
    await frameSelectedPeriod.click('[value=Listar]')
    const popup = await newPagePromise;
    await page.goto(popup.url())
    
    // 9 - Abre o conteúdo do texto (xml) em nova aba
    await checkIfLoadedThePage('a[href')
    page.click('a[href')
    
    // 10 - Pega o conteúdo do texto (xml) pra salvar xml
    await checkIfLoadedThePage('body pre')
    const notasFiscais = await page.evaluate( () => document.querySelector("body pre").textContent )

    // 11 - Salva o XML
    fs.writeFile('notas.xml', `<geral>${notasFiscais}</geral>`, (err) => { 
        if (err) throw err;
    })
    
    // await page.waitFor(2000)
    
    browser.close()
}

searchNFSeGoiania()