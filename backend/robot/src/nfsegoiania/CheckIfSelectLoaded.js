const path = require('path')
const createFolderToSaveData = require('../utils/CreateFolderToSaveData')

const CheckIfSelectLoaded = async(page, settingsProcessing) => {
    try {
        await page.waitForFunction(
            `document.querySelector('#GoianiaTheme_wtTelaPrincipal_block_wtTitle_wtDadosCAE').textContent.includes(${settingsProcessing.codigoPrefeitura})`
        )
        await page.waitFor(2500) // espera mais 2,5 segundos pra terminar de carregar os dados do novo select
    } catch (error) {
        console.log('\t[Final-Empresa] - Erro ao checar se a troca de empresa foi finalizada')
        console.log('\t-------------------------------------------------')
        const settings = { ...settingsProcessing, type: 'error' }
        let pathImg = createFolderToSaveData(settings)
        pathImg = path.join(pathImg, 'CheckIfSelectLoaded.png')
        await page.screenshot( { path: pathImg } )
        page.close()
        throw 'Error-CheckIfSelectLoaded'
    }
}

module.exports = CheckIfSelectLoaded