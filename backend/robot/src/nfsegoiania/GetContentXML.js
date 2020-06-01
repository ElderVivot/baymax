const path = require('path')
const createFolderToSaveData = require('../utils/CreateFolderToSaveData')

const GetContentXML = async(page, settingsProcessing) => {
    try {
        await page.waitFor('body pre')
        return await page.evaluate( () => document.querySelector("body pre").textContent )
    } catch (error) {
        console.log('\t[Final-Empresa] - Erro ao obter o conteúdo do XML')
        console.log('\t-------------------------------------------------')
        const settings = { ...settingsProcessing, type: 'error' }
        let pathImg = createFolderToSaveData(settings)
        pathImg = path.join(pathImg, 'GetContentXML.png')
        await page.screenshot( { path: pathImg } )
        page.close()
        throw 'Error-GetContentXML'
    }
}

module.exports = GetContentXML