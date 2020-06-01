const path = require('path')
const createFolderToSaveData = require('../utils/CreateFolderToSaveData')

const CheckIfExistNoteInPeriod = async(page, settingsProcessing) => {
    try {
        await page.waitFor('body')
        const body = await page.evaluate( () => {
            return document.querySelector('body').textContent
        })
        return body
    } catch (error) {
        console.log('\t[Final-Empresa] - Erro ao checar se existe nota no período')
        console.log('\t-------------------------------------------------')
        const settings = { ...settingsProcessing, type: 'error' }
        let pathImg = createFolderToSaveData(settings)
        pathImg = path.join(pathImg, 'CheckIfExistNoteInPeriod.png')
        await page.screenshot( { path: pathImg } )
        page.close()
        throw 'Error-CheckIfExistNoteInPeriod'
    }
}

module.exports = CheckIfExistNoteInPeriod