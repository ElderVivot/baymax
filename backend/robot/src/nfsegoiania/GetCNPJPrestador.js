const path = require('path')
const createFolderToSaveData = require('../utils/CreateFolderToSaveData')
const checkIfLoadedThePage = require('../utils/CheckIfLoadedThePage')

const GetCNPJPrestador = async(page, settingsProcessing) => {
    try {
        await checkIfLoadedThePage(page, 'cpo', isAFrame=true)
        const frame = page.frames().find(frame => frame.name() === 'cpo');
        await frame.waitFor('#nr_cnpj')
        let cpfCnpj = await frame.evaluate( () => {
            return document.querySelector('#nr_cnpj').textContent
        })
        cpfCnpj = cpfCnpj.replace(/[^\d]+/g,'')
        const { companies } = settingsProcessing
        if(companies.indexOf(cpfCnpj) < 0){
            throw 'IS_NOT_CLIENTE'
        }
        return cpfCnpj
    } catch (error) {
        let msgError = ''
        let type = 'error'
        if( error === "IS_NOT_CLIENTE"){
            console.log(`\t[14] - Empresa não é cliente desta Contabilidade neste período`)
            type = 'warning'            
            msgError = 'Warning-GetCNPJPrestador'
        } else {
            console.log('\t[Final-Empresa] - Erro ao checar o CNPJ/CPF')
            type = 'error'            
            msgError = 'Error-GetCNPJPrestador'
        }
        console.log('\t-------------------------------------------------')
        const settings = { ...settingsProcessing, type }
        let pathImg = createFolderToSaveData(settings)
        pathImg = path.join(pathImg, 'GetCNPJPrestador.png')
        await page.screenshot( { path: pathImg } )
        await page.close()
        throw msgError
    }
}

module.exports = GetCNPJPrestador