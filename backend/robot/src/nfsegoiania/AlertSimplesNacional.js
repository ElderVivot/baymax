const path = require('path')
const createFolderToSaveData = require('../utils/CreateFolderToSaveData')
const checkIfLoadedThePage = require('../utils/CheckIfLoadedThePage')

const AlertSimplesNacional = async(page, settingsProcessing) => {
    try {
        await checkIfLoadedThePage(page, 'cpo', isAFrame=true)
        const frame = page.frames().find(frame => frame.name() === 'cpo')
        await frame.waitFor('center a')
        await frame.click('center a')
    } catch (error) {
        console.log('\t[Final-Empresa] - Erro ao passar pelo alerta do simples nacional.')
        console.log('\t-------------------------------------------------')
        const settings = { ...settingsProcessing, type: 'error' }
        let pathImg = createFolderToSaveData(settings)
        pathImg = path.join(pathImg, 'AlertSimplesNacional.png')
        await page.screenshot( { path: pathImg } )
        await page.close()
        throw 'Error-AlertSimplesNacional'
    }
}

module.exports = AlertSimplesNacional