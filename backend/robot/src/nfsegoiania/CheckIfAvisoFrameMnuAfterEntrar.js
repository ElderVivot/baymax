const path = require('path')
const createFolderToSaveData = require('../utils/CreateFolderToSaveData')
const checkIfLoadedThePage = require('../utils/CheckIfLoadedThePage')

const CheckIfAvisoFrameMnuAfterEntrar = async(page, settingsProcessing) => {
    try {
        await checkIfLoadedThePage(page, 'mnu', isAFrame=true)
        const frame = page.frames().find(frame => frame.name() === 'mnu')
        await frame.waitFor('tr[bgcolor=beige] > td > table > tbody > tr > td[align=center] > span')
        const aviso = await frame.evaluate( () => {
            return document.querySelector('tr[bgcolor=beige] > td > table > tbody > tr > td[align=center] > span').textContent
        })
        return aviso
    } catch (error) {
        console.log('\t[Final-Empresa] - Erro ao verificar se a empresa está habilitada pra emitir NFS-e Serviço')
        console.log('\t-------------------------------------------------')
        const settings = { ...settingsProcessing, type: 'error' }
        let pathImg = createFolderToSaveData(settings)
        pathImg = path.join(pathImg, 'CheckIfAvisoFrameMnuAfterEntrar.png')
        await page.screenshot( { path: pathImg } )
        page.close()
        throw 'Error-CheckIfAvisoFrameMnuAfterEntrar'
    }
}

module.exports = CheckIfAvisoFrameMnuAfterEntrar