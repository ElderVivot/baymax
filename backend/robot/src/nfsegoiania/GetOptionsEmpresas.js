const path = require('path')
const createFolderToSaveData = require('../utils/CreateFolderToSaveData')

const GetOptionsEmpresas = async(page, browser, settingsProcessing) => {
    try {
        await page.waitFor('#GoianiaTheme_wtTelaPrincipal_block_wtActions_SISEGIntegration_wt104_block_wtAcessos')
        const optionsEmpresas = await page.evaluate( () => {
            let options = []
            const optionsAll = document.querySelectorAll('#GoianiaTheme_wtTelaPrincipal_block_wtActions_SISEGIntegration_wt104_block_wtAcessos > option')
            optionsAll.forEach( value => {
                if(value.textContent !== "Informe a Empresa"){
                    let labelSplit = value.textContent.split('-')
                    let label = ''
                    let codigoPrefeitura = '' // este código aparentemente é inscrição municipal
                    if(labelSplit.length > 1){
                        const nameEmpresaSplit = labelSplit.slice(1, labelSplit.length)
                        codigoPrefeitura = labelSplit[0].replace(/[^\d]+/g,'')

                        const nameEmpresa = nameEmpresaSplit.join('').trim().replace(/([\u0300-\u036f]|[^0-9a-zA-Z\ ])/g, '').toUpperCase().substring(0, 50)

                        label = `${nameEmpresa} - ${codigoPrefeitura}`
                    } else {
                        label = labelSplit[0]
                        codigoPrefeitura = labelSplit[0].replace(/[^\d]+/g,'')
                    }
                    options.push({
                        value: value.getAttribute('value'),
                        label: label,
                        codigoPrefeitura: codigoPrefeitura
                    })
                }
            } )
            return options
        })
        return optionsEmpresas
    } catch (error) {
        console.log('[Final-Loguin] - Erro ao pegar lista de empresas que este loguin tem acesso')
        const settings = { ...settingsProcessing, type: 'error' }
        let pathImg = createFolderToSaveData(settings)
        pathImg = path.join(pathImg, 'GetOptionsEmpresas.png')
        await page.screenshot( { path: pathImg } )
        browser.close()
        throw 'Error-GetOptionsEmpresas'
    }
}

module.exports = GetOptionsEmpresas