const fs = require('fs')
const path = require('path')
const createFolderToSaveData = require('../utils/CreateFolderToSaveData')

const SaveXML = async(content, settingsProcessing) => {
    const settings = { ...settingsProcessing, type: 'sucess' }
    let pathNote = createFolderToSaveData(settings)
    pathNote = path.join(pathNote, `${settingsProcessing.cpfCnpj}.xml`)
    fs.writeFile(pathNote, `<geral>${content}</geral>`, async(err) => { 
        if (err) {
            console.log('\t[Final-Empresa] - Erro ao salvar XML')
            console.log('\t-------------------------------------------------')
            settings[type] = 'error'
            let pathImg = createFolderToSaveData(settings)
            pathImg = path.join(pathImg, 'SaveXML.png')
            await page.screenshot( { path: pathImg } )
            await page.close()
            throw 'Error-SaveXML'
        }
    }) 
}

module.exports = SaveXML