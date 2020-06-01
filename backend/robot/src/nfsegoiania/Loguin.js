const path = require('path')
const createFolderToSaveData = require('../utils/CreateFolderToSaveData')

const Loguin = async(page, loguin, password, browser, settingsProcessing) => {
    try {
        await page.waitFor('#wt38_wtLoginContent_wtUserNameInput')
        await page.type('#wt38_wtLoginContent_wtUserNameInput', loguin)
        await page.type('#wt38_wtLoginContent_wtPasswordInput', password)
        await page.click('#wt38_wtLoginContent_wt8')
        await page.waitFor(2000)

        let userInvalid = false
        try {
            userInvalid = await page.evaluate( () => {
                return document.querySelector('#wt38_WebPatterns_wt5_block_RichWidgets_wt9_block_wtSanitizedHtml2').textContent
            } )
        } catch (error) {
            userInvalid = false
        }        

        if(userInvalid !== false){
            throw 'Usuário ou Senha Inválida'
        }
    } catch (error) {
        if(error === 'Usuário ou Senha Inválida'){
            console.log('[Final-Loguin] - Usuário ou senha inválida')
        } else {
            console.log('[Final-Loguin] - Erro ao fazer Loguin')
        }
        const settings = { ...settingsProcessing, type: 'error' }
        let pathImg = createFolderToSaveData(settings)
        pathImg = path.join(pathImg, 'Loguin.png')
        await page.screenshot( { path: pathImg } )
        browser.close()
        throw 'Error-Loguin'
    }
}

module.exports = Loguin