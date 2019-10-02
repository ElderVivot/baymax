const puppeteer = require('puppeteer')

const buscaNFSeGoiania = async() => {
    const browser = await puppeteer.launch({headless: !(true)})

    const page = await browser.newPage()

    await page.setViewport({ width:1366, height:768 })

    // 1 - Acessa página de Goiânia
    await page.goto('https://www10.goiania.go.gov.br/Internet/Login.aspx')
    
    // 2 - Faz loguin
    await page.type('#wt38_wtLoginContent_wtUserNameInput', '02229419102')
    await page.type('#wt38_wtLoginContent_wtPasswordInput', 'soma100')
    await page.click('#wt38_wtLoginContent_wt8')
    // await page.waitForNavigation()
    
    // 3 - Clica no botão Portal do Contribuinte
    await page.goto('https://www10.goiania.go.gov.br/SicaePortal/')

    const teste = await page.content()
    console.log(teste)

    // 4 - Abre a página da DMS
    // try {
    //     const newLink = await page.evaluate( 
    //         () => document.querySelector('#GoianiaTheme_wtTelaPrincipal_block_wtMainContent_wt25_WebPatterns_wt11_block_wtText_wtDMS')
    //     );
    //     console.log(newLink)
    // }catch(error){
    //     console.log('- Não foi possível abrir a página DMS.' + error)
    // }

    browser.close()
}

buscaNFSeGoiania()