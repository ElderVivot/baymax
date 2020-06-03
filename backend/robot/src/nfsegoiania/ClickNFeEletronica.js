const path = require('path')
const createFolderToSaveData = require('../utils/CreateFolderToSaveData')

const ClickNFeEletronica = async(page, settingsProcessing) => {
    try {
        await page.waitFor('#GoianiaTheme_wtTelaPrincipal_block_wtMainContent_WebPatterns_wt157_block_wtContent1_wt54_WebPatterns_wt370_block_wtContent_WebPatterns_wt477_block_wtText_wtNFEletronica')
        await page.click('#GoianiaTheme_wtTelaPrincipal_block_wtMainContent_WebPatterns_wt157_block_wtContent1_wt54_WebPatterns_wt370_block_wtContent_WebPatterns_wt477_block_wtText_wtNFEletronica', {waitUntil: 'domcontentloaded'})
    } catch (error) {
        console.log('\t[Final-Empresa] - Erro ao clicar no botão "NF-e Eletrônica"')
        console.log('\t-------------------------------------------------')
        const settings = { ...settingsProcessing, type: 'error' }
        let pathImg = createFolderToSaveData(settings)
        pathImg = path.join(pathImg, 'ClickNFeEletronica.png')
        await page.screenshot( { path: pathImg } )
        await page.close()
        throw 'Error-ClickNFeEletronica'
    }
}

module.exports = ClickNFeEletronica