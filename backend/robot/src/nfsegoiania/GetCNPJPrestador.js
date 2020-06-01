const path = require('path')
const createFolderToSaveData = require('../utils/CreateFolderToSaveData')
const checkIfLoadedThePage = require('../utils/CheckIfLoadedThePage')

const GetCNPJPrestador = async(page, settingsProcessing) => {
    try {
        await checkIfLoadedThePage(page, 'cpo', isAFrame=true)
        const frame = page.frames().find(frame => frame.name() === 'cpo');
        await frame.waitFor('#nr_cnpj')
        const cnpjCpf = await frame.evaluate( () => {
            return document.querySelector('#nr_cnpj').textContent
        })
        return cnpjCpf.replace(/[^\d]+/g,'')
    } catch (error) {
        console.log('\t[Final-Empresa] - Erro ao pegar o CNPJ/CPF')
        console.log('\t-------------------------------------------------')
        const settings = { ...settingsProcessing, type: 'error' }
        let pathImg = createFolderToSaveData(settings)
        pathImg = path.join(pathImg, 'GetCNPJPrestador.png')
        await page.screenshot( { path: pathImg } )
        page.close()
        throw 'Error-GetCNPJPrestador'
    }
}

module.exports = GetCNPJPrestador