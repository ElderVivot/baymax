const path = require('path')
const createFolderToSaveData = require('../utils/CreateFolderToSaveData')

const ClickToOpenContentXML = async(page, settingsProcessing) => {
    try {
        await page.waitFor('a[href]')
        await page.click('a[href]')
    } catch (error) {
        console.log('\t[Final-Empresa] - Erro ao abrir o conteúdo do XML')
        console.log('\t-------------------------------------------------')
        const settings = { ...settingsProcessing, type: 'error' }
        let pathImg = createFolderToSaveData(settings)
        pathImg = path.join(pathImg, 'ClickToOpenContentXML.png')
        await page.screenshot( { path: pathImg } )
        page.close()
        throw 'Error-ClickToOpenContentXML'
    }
}

module.exports = ClickToOpenContentXML