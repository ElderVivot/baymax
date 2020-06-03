const path = require('path')
const createFolderToSaveData = require('../utils/CreateFolderToSaveData')

const GotoLinkNFeEletrotinaEntrar = async(page, settingsProcessing) => {
    let urlButtonEntrar = ''
    try {
        await page.waitFor('#GoianiaTheme_wtTelaPrincipal_block_wtMainContent_WebPatterns_wt157_block_wtContent1_wt54_WebPatterns_wt70_block_wtContent_wt298')
        
        urlButtonEntrar = await page.evaluate( 
            () => document.querySelector('#GoianiaTheme_wtTelaPrincipal_block_wtMainContent_WebPatterns_wt157_block_wtContent1_wt54_WebPatterns_wt70_block_wtContent_wt298').getAttribute('href')
        )
        // o then é pra passar pelo alert
        await page.goto(urlButtonEntrar).then(
            await page.on('dialog', async dialog => {
                await dialog.accept()
            })
        )
    } catch (e) {
        console.log('\t[Final-Empresa] - Erro ao abrir o link do "NF-e Eletrônica" e passar pelo Alert')
        console.log('\t-------------------------------------------------')
        const settings = { ...settingsProcessing, type: 'error' }
        let pathImg = createFolderToSaveData(settings)
        pathImg = path.join(pathImg, 'GotoLinkNFeEletrotinaEntrar.png')
        await page.screenshot( { path: pathImg } )
        await page.close()
        throw 'Error-GotoLinkNFeEletrotinaEntrar'
    }
}

module.exports = GotoLinkNFeEletrotinaEntrar