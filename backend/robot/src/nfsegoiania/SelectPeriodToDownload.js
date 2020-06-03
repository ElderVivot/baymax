const path = require('path')
const createFolderToSaveData = require('../utils/CreateFolderToSaveData')
const checkIfLoadedThePage = require('../utils/CheckIfLoadedThePage')

const SelectPeriodToDownload = async(page, settingsProcessing) => {
    try {
        await checkIfLoadedThePage(page, 'cpo', isAFrame=true)
        const frame = page.frames().find(frame => frame.name() === 'cpo');
        await frame.waitFor('[name=txt_dia_inicial]')
        await frame.select('[name=txt_dia_inicial]', "01")
        await frame.select('[name=txt_dia_final]', "31")
        await frame.select('[name=sel_mes]', "05")
        await frame.type('[name=txt_ano]', "2020")
    } catch (error) {
        console.log('\t[Final-Empresa] - Erro ao selecionar o período')
        console.log('\t-------------------------------------------------')
        const settings = { ...settingsProcessing, type: 'error' }
        let pathImg = createFolderToSaveData(settings)
        pathImg = path.join(pathImg, 'SelectPeriodToDownload.png')
        await page.screenshot( { path: pathImg } )
        await page.close()
        throw 'Error-SelectPeriodToDownload'
    }
}

module.exports = SelectPeriodToDownload