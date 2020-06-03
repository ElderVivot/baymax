const path = require('path')
const createFolderToSaveData = require('../utils/CreateFolderToSaveData')

const OpenSiteGoiania = async(page, browser, settingsProcessing) => {
    try {
        await page.goto('https://www10.goiania.go.gov.br/Internet/Login.aspx', {timeout: 10000})
    } catch (error) {
        console.log('[Final-Loguin] - Erro ao abrir site de Goiânia')
        const settings = { ...settingsProcessing, type: 'error' }
        let pathImg = createFolderToSaveData(settings)
        pathImg = path.join(pathImg, 'OpenSiteGoiania.png')
        await page.screenshot( { path: pathImg } )
        await browser.close()
        throw 'Error-OpenSiteGoiania'
    }
}

module.exports = OpenSiteGoiania