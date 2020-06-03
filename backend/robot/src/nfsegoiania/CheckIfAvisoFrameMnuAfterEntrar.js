const path = require('path')
const createFolderToSaveData = require('../utils/CreateFolderToSaveData')
const checkIfLoadedThePage = require('../utils/CheckIfLoadedThePage')

const CheckIfAvisoFrameMnuAfterEntrar = async(page, settingsProcessing) => {
    let aviso = ''
    try {
        await checkIfLoadedThePage(page, 'mnu', isAFrame=true)
        const frame = page.frames().find(frame => frame.name() === 'mnu')
        await frame.waitFor('tr[bgcolor=beige] > td > table > tbody > tr > td[align=center] > span')
        aviso = await frame.evaluate( () => {
            return document.querySelector('tr[bgcolor=beige] > td > table > tbody > tr > td[align=center] > span').textContent
        })
        aviso = aviso.normalize("NFD").replace(/[^a-zA-Z/ ]/g, "").toUpperCase()
        if( aviso.trim() !== "" ){
            throw "NAO_HABILITADA_EMITIR_NFSE"
        }
    } catch (error) {
        let msgError = ''
        let type = 'error'
        if( error === "NAO_HABILITADA_EMITIR_NFSE"){
            console.log(`\t[Final-Empresa] - Empresa não habilitada pra emitir NFS-e. O aviso é "${aviso}". Fechando aba.`)
            type = 'warning'            
            msgError = 'Warning-CheckIfAvisoFrameMnuAfterEntrar'
        } else {
            console.log('\t[Final-Empresa] - Erro ao verificar se a empresa está habilitada pra emitir NFS-e Serviço')            
            type = 'error'            
            msgError = 'Error-CheckIfAvisoFrameMnuAfterEntrar'
        }
        console.log('\t-------------------------------------------------')
        const settings = { ...settingsProcessing, type }
        let pathImg = createFolderToSaveData(settings)
        pathImg = path.join(pathImg, 'CheckIfAvisoFrameMnuAfterEntrar.png')
        await page.screenshot( { path: pathImg } )
        await page.close()
        throw msgError
    }
}

module.exports = CheckIfAvisoFrameMnuAfterEntrar