const path = require('path')
const createFolderToSaveData = require('../utils/CreateFolderToSaveData')

const CheckIfExistNoteInPeriod = async(page, settingsProcessing) => {
    try {
        await page.waitFor('body')
        let aviso = await page.evaluate( () => {
            return document.querySelector('body').textContent
        })
        aviso = aviso.normalize("NFD").replace(/[^a-zA-Z/ -]/g, "").toUpperCase()
        if( aviso.indexOf('NENHUMA NFS-E ENCONTRADA') >= 0 ){
            throw "NOT_EXIST_NFSE"
        }
    } catch (error) {
        let msgError = ''
        let type = 'error'
        if( error === "NOT_EXIST_NFSE"){
            console.log(`\t[16] - Não há nenhuma nota no filtro passado`)
            type = 'warning'            
            msgError = 'Warning-CheckIfExistNoteInPeriod'
        } else {
            console.log('\t[Final-Empresa] - Erro ao checar se existe nota no período')
            type = 'error'            
            msgError = 'Error-CheckIfExistNoteInPeriod'
        }
        console.log('\t-------------------------------------------------')
        const settings = { ...settingsProcessing, type }
        let pathImg = createFolderToSaveData(settings)
        pathImg = path.join(pathImg, 'CheckIfExistNoteInPeriod.png')
        await page.screenshot( { path: pathImg } )
        await page.close()
        throw msgError
    }
}

module.exports = CheckIfExistNoteInPeriod