const path = require('path')
const createFolderToSaveData = require('../utils/CreateFolderToSaveData')
const checkIfLoadedThePage = require('../utils/CheckIfLoadedThePage')

const ClickDownloadXML = async(page, settingsProcessing) => {
    try {
        await checkIfLoadedThePage(page, 'cpo', isAFrame=true)
        const frame = page.frames().find(frame => frame.name() === 'cpo')
        await frame.waitFor("tr td font a[href*='snfse00200f3']")
        await frame.click("tr td font a[href*='snfse00200f3']")
    } catch (error) {
        console.log('\t[Final-Empresa] - Erro ao clicar no botão "Download de XML de Notas Fiscais por período".')
        console.log('\t-------------------------------------------------')
        const settings = { ...settingsProcessing, type: 'error' }
        let pathImg = createFolderToSaveData(settings)
        pathImg = path.join(pathImg, 'ClickDownloadXML.png')
        await page.screenshot( { path: pathImg } )
        page.close()
        throw 'Error-ClickDownloadXML'
    }
}

module.exports = ClickDownloadXML