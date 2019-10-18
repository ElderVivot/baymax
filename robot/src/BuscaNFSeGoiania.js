const puppeteer = require('puppeteer')

const buscaNFSeGoiania = async() => {
    const browser = await puppeteer.launch({headless: !(true)})

    const page = await browser.newPage()

    await page.setViewport({ width:1366, height:768 })

    // 1 - Acessa página de Goiânia
    await page.goto('https://www10.goiania.go.gov.br/Internet/Login.aspx')
    
    // 2 - Faz loguin
    await page.type('#wt38_wtLoginContent_wtUserNameInput', '02319085122')
    await page.type('#wt38_wtLoginContent_wtPasswordInput', '3771814')
    await page.click('#wt38_wtLoginContent_wt8')

    await page.waitFor(1000)

    // 3 - clicando no botão portal do Contribuinte
    const positionPortalContribuinte = await page.evaluate( () => {
        function offset(el) {
            let rect = el.getBoundingClientRect(),
            scrollLeft = window.pageXOffset || document.documentElement.scrollLeft,
            scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            return { top: rect.top + scrollTop, left: rect.left + scrollLeft }
        }

        let elementSelected = document.querySelector('#GoianiaTheme_wt27_block_wtMainContent_wtSistemaTable_ctl03_wt28');
        let elementSelectedOffset = offset(elementSelected);
        console.log(elementSelectedOffset.left, elementSelectedOffset.top);
        return [elementSelectedOffset.left, elementSelectedOffset.top]
    })

    console.log(positionPortalContribuinte[0], positionPortalContribuinte[1])

    await page.mouse.click(positionPortalContribuinte[0], positionPortalContribuinte[1])

    await page.waitFor(5000)

    // --------------------------------------

    // 4 - clicando no botão Nota Fiscal
    const positionDMS = await page.evaluate( () => {
        function offset(el) {
            let rect = el.getBoundingClientRect(),
            scrollLeft = window.pageXOffset || document.documentElement.scrollLeft,
            scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            return { top: rect.top + scrollTop, left: rect.left + scrollLeft }
        }

        let elementSelected = document.querySelector('#GoianiaTheme_wtTelaPrincipal_block_wtMainContent_wt25_WebPatterns_wt72_block_wtText_wtNFEletronica');
        let elementSelectedOffset = offset(elementSelected);
        console.log(elementSelectedOffset.left, elementSelectedOffset.top);
        return [elementSelectedOffset.left, elementSelectedOffset.top]
    })

    console.log(positionDMS[0], positionDMS[1])

    await page.mouse.click(positionDMS[0], positionDMS[1])

    await page.waitFor(3000)

    // 5 - Abre a página da Nota Fiscal
    try {
        const newLink = await page.evaluate( 
            () => document.querySelector('#GoianiaTheme_wtTelaPrincipal_block_wtMainContent_wt25_WebPatterns_wt50_block_wtContent_wt229').getAttribute('href')
        );
        console.log(newLink)
        await page.goto(newLink).then(
            await page.on('dialog', async dialog => {
                await dialog.accept()
            }) 
        )
    } catch (e) {
        console.log(e)
    }

    await page.waitFor(3000)

    // 5 - Abre a página da Nota Fiscal
    try {
        const urlBase = page.url()
        const urlNavigator = urlBase.split('sistemas')
        console.log(urlNavigator)
        await page.goto(`${urlNavigator[0]}/sistemas/snfse/asp/snfse00000f2.asp`)
    } catch (e) {
        console.log(e)
    }

    await page.waitFor(3000)

    // const teste = await page.content()
    // console.log(teste)

    // try {
        const newLink = await page.evaluate( () => {
            let options = Array.from(document.querySelectorAll("tr td font b"));
            let optionSelected = options.filter(option => option.textContext == "Download de XML de Notas Fiscais por período")
            console.log(options, optionSelected)
            let link = optionSelected[0].baseURI
            return link
        });
        console.log(newLink)
        await page.goto(newLink)
    // } catch (e) {
    //     console.log(e)
    // }

    // browser.close()
}

buscaNFSeGoiania()