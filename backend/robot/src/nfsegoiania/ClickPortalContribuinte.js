const path = require('path')
const createFolderToSaveData = require('../utils/CreateFolderToSaveData')

const ClickPortalContribuinte = async(page, browser) => {
    try {
        await page.waitFor('#GoianiaTheme_wt27_block_wtMainContent_wtSistemaTable')
        const IDTablePortalContribuinte = await page.evaluate( () => {
            const trs = document.querySelectorAll('#GoianiaTheme_wt27_block_wtMainContent_wtSistemaTable > tbody > tr')
            let id = ''
            trs.forEach( value => {
                const tagA = value.getElementsByTagName('a')[0]
                if(tagA.textContent == "Portal do Contribuinte"){
                    id = tagA.getAttribute('id')
                }
            })
            return id
        })
        await page.click(`#${IDTablePortalContribuinte}`)
    } catch (error) {
        console.log('[Final-Loguin] - Erro ao clicar no botão "Portal do Contruibnte"')
        const settings = { ...settingsProcessing, type: 'error' }
        let pathImg = createFolderToSaveData(settings)
        pathImg = path.join(pathImg, 'ClickPortalContribuinte.png')
        await page.screenshot( { path: pathImg } )
        await browser.close()
        throw 'Error-ClickPortalContribuinte'
    }
}

module.exports = ClickPortalContribuinte