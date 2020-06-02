const path = require('path')
const createFolderToSaveData = require('../utils/CreateFolderToSaveData')

const ClickListarXML = async(page, newPagePromise, settingsProcessing) => {
    try {
        const frame = page.frames().find(frame => frame.name() === 'cpo');
        await frame.waitFor('[value=Listar]')
        await frame.click('[value=Listar]')
        const popup = await newPagePromise;
        await page.goto(popup.url(), {waitUntil: 'load', timeout: 600000}) // aguarda até 10 minutos carregar a página pra fazer o download
    } catch (error) {
        console.log('\t[Final-Empresa] - Erro ao listar os XMLs')
        console.log('\t-------------------------------------------------')
        const settings = { ...settingsProcessing, type: 'error' }
        let pathImg = createFolderToSaveData(settings)
        pathImg = path.join(pathImg, 'ClickListarXML.png')
        await page.screenshot( { path: pathImg } )
        page.close()
        throw 'Error-ClickListarXML'
    }
}

module.exports = ClickListarXML