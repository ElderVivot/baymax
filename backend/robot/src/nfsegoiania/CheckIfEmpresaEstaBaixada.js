const path = require('path')
const createFolderToSaveData = require('../utils/CreateFolderToSaveData')

const CheckIfEmpresaEstaBaixada = async(page, settingsProcessing) => {
    try {
        await page.waitFor('#GoianiaTheme_wtTelaPrincipal_block_wtMainContent_WebPatterns_wt157_block_wtContent1_wtLinks')
        const aviso = await page.evaluate( () => {
            return document.querySelector('#GoianiaTheme_wtTelaPrincipal_block_wtMainContent_WebPatterns_wt157_block_wtContent1_wtLinks > div:nth-child(1)').textContent
        })
        return aviso.replace(/([\u0300-\u036f]|[^0-9a-zA-Z])/g, '')
    } catch (error) {
        console.log(error)
        console.log('\t[Final-Empresa] - Erro ao verificar se a empresa está com o status "Baixa"')
        console.log('\t-------------------------------------------------')
        const settings = { ...settingsProcessing, type: 'error' }
        let pathImg = createFolderToSaveData(settings)
        pathImg = path.join(pathImg, 'CheckIfEmpresaEstaBaixada.png')
        await page.screenshot( { path: pathImg } )
        page.close()
        throw 'Error-CheckIfEmpresaEstaBaixada'
    }
}

module.exports = CheckIfEmpresaEstaBaixada