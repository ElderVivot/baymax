const path = require('path')
const createFolderToSaveData = require('../utils/CreateFolderToSaveData')

const CheckIfEmpresaEstaBaixada = async(page, settingsProcessing) => {
    try {
        await page.waitFor('#GoianiaTheme_wtTelaPrincipal_block_wtMainContent_WebPatterns_wt157_block_wtContent1_wtLinks')
        let aviso = await page.evaluate( () => {
            return document.querySelector('#GoianiaTheme_wtTelaPrincipal_block_wtMainContent_WebPatterns_wt157_block_wtContent1_wtLinks > div:nth-child(1)').textContent
        })
        aviso = aviso.normalize("NFD").replace(/[^a-zA-Z/ ]/g, "").toUpperCase()
        if(aviso.indexOf('SITUACAO BAIXA') >= 0 || aviso.indexOf('SITUACAO SUSPENSAO') >= 0){
            throw "BAIXADA_SUSPENSA"
        }
    } catch (error) {
        let msgError = ''
        let type = 'error'
        if(error === "BAIXADA_SUSPENSA"){
            console.log(`\t[Final-Empresa] - Esta empresa está com situação "Baixada/Suspensa" na prefeitura. Fechando aba.`)
            type = 'warning'
            msgError = 'Warning-CheckIfEmpresaEstaBaixada'      
        } else {
            console.log('\t[Final-Empresa] - Erro ao verificar se a empresa está com o status "Baixa"')
            type = 'error'
            msgError = 'Error-CheckIfEmpresaEstaBaixada'          
        }        
        console.log('\t-------------------------------------------------')
        const settings = { ...settingsProcessing, type }
        let pathImg = createFolderToSaveData(settings)
        pathImg = path.join(pathImg, 'CheckIfEmpresaEstaBaixada.png')
        await page.screenshot( { path: pathImg } )
        await page.close()
        throw msgError
    }
}

module.exports = CheckIfEmpresaEstaBaixada