const puppeteer = require('puppeteer')
const path = require('path')
const createFolderToSaveData = require('../utils/CreateFolderToSaveData')
const OpenSiteGoiania = require('./OpenSiteGoiania')
const Loguin = require('./Loguin')
const ClickPortalContribuinte = require('./ClickPortalContribuinte')
const GetOptionsEmpresas = require('./GetOptionsEmpresas')
const CheckIfEmpresaEstaBaixada = require('./CheckIfEmpresaEstaBaixada')
const ClickNFeEletronica = require('./ClickNFeEletronica')
const GotoLinkNFeEletrotinaEntrar = require('./GotoLinkNFeEletrotinaEntrar')
const CheckIfAvisoFrameMnuAfterEntrar = require('./CheckIfAvisoFrameMnuAfterEntrar')
const AlertSimplesNacional = require('./AlertSimplesNacional')
const ClickDownloadXML = require('./ClickDownloadXML')
const GetCNPJPrestador = require('./GetCNPJPrestador')
const SelectPeriodToDownload = require('./SelectPeriodToDownload')
const ClickListarXML = require('./ClickListarXML')
const CheckIfExistNoteInPeriod = require('./CheckIfExistNoteInPeriod')
const ClickToOpenContentXML = require('./ClickToOpenContentXML')
const GetContentXML = require('./GetContentXML')
const SaveXML = require('./SaveXML')
const CloseOnePage = require('./CloseOnePage')

// loguin='02319085122', password='3771814'
// loguin='73470384134', password='soma100'
const MainNfseGoiania = async(settingsPrincipal) => {
    const { loguin, password, companies } = settingsPrincipal
    const settingsProcessing = { ...settingsPrincipal }

    try {
        console.log(`[0] - Abrindo loguin ${loguin}`)
        
        const browser = await puppeteer.launch({headless: false, args: ['--start-maximized']})
        const page = await browser.newPage()
        await page.setViewport({ width:0, height:0 })  

        // 1 - Acessa página de Goiânia
        console.log(`[1] - Abrindo site da prefeitura`)
        await OpenSiteGoiania(page, browser, settingsProcessing)
        
        // 2 - Faz loguin
        console.log(`[2] - Realizando o loguin`)
        await Loguin(page, loguin, password, browser, settingsProcessing)
        
        // 3 - Clica no botão portal do contribuinte
        console.log(`[3] - Clicando no botão "Portal Contruinte"`)
        await ClickPortalContribuinte(page, browser, settingsProcessing)

        // 4 - Seleciona as empresas que a pessoa tem acesso
        console.log(`[4] - Pegando a relação de empresas que este contribuinte possui.`)
        const optionsEmpresas = await GetOptionsEmpresas(page, browser, settingsProcessing)

        // 5 - pega a URL atual pra não ter que abrir do zero o processo
        urlActual = page.url()

        // 6 - Percorre o array de empresas
        for(option of optionsEmpresas){
            console.log(`\t[5] - Iniciando processamento da empresa ${option.label}`)

            settingsProcessing['valueEmpresa'] = option.value
            settingsProcessing['labelEmpresa'] = option.label
                        
            try {        
                // 7 - Abre uma nova aba no navegador e navega pra página atual
                const pageEmpresa = await browser.newPage()
                await pageEmpresa.setViewport({ width:0, height:0 })
                await pageEmpresa.goto(urlActual)

                // 8 - Seleciona a empresa
                await pageEmpresa.waitFor('#GoianiaTheme_wtTelaPrincipal_block_wtActions_SISEGIntegration_wt104_block_wtAcessos')
                await pageEmpresa.select('#GoianiaTheme_wtTelaPrincipal_block_wtActions_SISEGIntegration_wt104_block_wtAcessos', option.value)
                // esperar aparecer o nome da empresa
                await pageEmpresa.waitForFunction(
                    `document.querySelector('#GoianiaTheme_wtTelaPrincipal_block_wtTitle_wtDadosCAE').textContent.includes(${option.codigoPrefeitura})`
                )
                await pageEmpresa.waitFor(2000) // espera mais dois segundos pra terminar de carregar os dados do novo select
                
                // 9 - Verificando se o "Contribuinte está com a situação Baixa"
                console.log(`\t[6] - Verificando se o "Contribuinte está com a situação Baixa"`)
                const avisoEmpresaBaixada = await CheckIfEmpresaEstaBaixada(pageEmpresa, settingsProcessing)
                if(avisoEmpresaBaixada.toUpperCase().indexOf('SITUACAO BAIXA') >= 0){
                    console.log(`\t[7] - Esta empresa está com situação "Baixada" na prefeitura`)
                    const settings = { ...settingsProcessing, type: 'warning' }
                    let pathImg = createFolderToSaveData(settings)
                    pathImg = path.join(pathImg, 'CheckIfEmpresaEstaBaixada.png')
                    await pageEmpresa.screenshot( { path: pathImg } )
                    await CloseOnePage(pageEmpresa)
                    continue
                }

                // 10 - Clicando no botão NF-e Eletrônica
                console.log(`\t[7] - Clicando no botão "NF-e Eletrônica"`)
                await ClickNFeEletronica(pageEmpresa, settingsProcessing)

                // 11 - Abre o link do botão "Entrar"
                console.log(`\t[8] - Clicando no botão "Entrar"`)
                await GotoLinkNFeEletrotinaEntrar(pageEmpresa, settingsProcessing)

                // 12 - Aviso depois do botão "Entrar" --> caso tenha aviso para o processamento desta
                // empresa, pois geralmente quando tem é empresa sem atividade de serviço ou usuário inválido        
                const avisoFrameMnuAfterEntrar = await CheckIfAvisoFrameMnuAfterEntrar(pageEmpresa, settingsProcessing)
                if( avisoFrameMnuAfterEntrar.trim() !== "" ){
                    console.log(`\t[9] - Empresa não habilitada pra emitir NFS-e. O aviso é ${avisoFrameMnuAfterEntrar}`)
                    const settings = { ...settingsProcessing, type: 'warning' }
                    let pathImg = createFolderToSaveData(settings)
                    pathImg = path.join(pathImg, 'CheckIfAvisoFrameMnuAfterEntrar.png')
                    await pageEmpresa.screenshot( { path: pathImg } )
                    await CloseOnePage(pageEmpresa)
                    continue
                }

                // 13 - Passa pelo Alerta do Simples Nacional
                console.log(`\t[9] - Passando pelo alerta do simples nacional.`)
                await AlertSimplesNacional(pageEmpresa, settingsProcessing)

                // 14 - Clica no botão "Download de XML de Notas Fiscais por período"
                console.log(`\t[10] - Clicando no botão "Download de XML de Notas Fiscais por período"`)
                await ClickDownloadXML(pageEmpresa, settingsProcessing)

                // 15 - Analisa se o CNPJ é de cliente válido
                console.log(`\t[11] - Analisando se o CNPJ/CPF do Prestador é cliente desta Contabilidade`)
                const cpfCnpj = await GetCNPJPrestador(pageEmpresa, settingsProcessing)
                if(companies.indexOf(cpfCnpj) < 0){
                    console.log(`\t[12] - Empresa não é cliente desta Contabilidade neste período`)
                    const settings = { ...settingsProcessing, type: 'warning' }
                    let pathImg = createFolderToSaveData(settings)
                    pathImg = path.join(pathImg, 'GetCNPJPrestador.png')
                    await pageEmpresa.screenshot( { path: pathImg } )
                    await CloseOnePage(pageEmpresa)
                    continue
                }

                settingsProcessing['cpfCnpj'] = cpfCnpj

                // 16 - Seleciona o Período pra download
                console.log(`\t[12] - Seleciona o período desejado pra baixar os XMLs`)
                await SelectPeriodToDownload(pageEmpresa, settingsProcessing)

                // 17 - Clica no botão "Listar"
                console.log(`\t[13] - Clicando no botão "Listar"`)
                const newPagePromise = new Promise(resolve => {
                    browser.once('targetcreated', target => resolve(target.page()))
                })
                await ClickListarXML(pageEmpresa, newPagePromise, settingsProcessing)
                
                // 18 - Verifica se tem notas no período solicitado, caso não, para o processamento
                const existNotes = await CheckIfExistNoteInPeriod(pageEmpresa, settingsProcessing)
                if(existNotes.toUpperCase().indexOf('NENHUMA NFS-E ENCONTRADA') >= 0){
                    console.log(`\t[14] - Não há nenhuma nota no filtro passado`)
                    const settings = { ...settingsProcessing, type: 'warning' }
                    let pathImg = createFolderToSaveData(settings)
                    pathImg = path.join(pathImg, 'CheckIfExistNoteInPeriod.png')
                    await pageEmpresa.screenshot( { path: pathImg } )
                    await CloseOnePage(pageEmpresa)
                    continue
                }
                
                // 19 - Abre o conteúdo do XML
                console.log(`\t[14] - Abrindo os dados das notas`)
                await ClickToOpenContentXML(pageEmpresa, settingsProcessing)

                // 20 - Pega conteúdo do XML
                console.log(`\t[15] - Obtendo conteúdo das notas`)
                const contentXML = await GetContentXML(pageEmpresa, settingsProcessing)

                // 21 - Salva o XML
                console.log(`\t[16] - Salvando XML das notas`)
                await SaveXML(contentXML, settingsProcessing)

                // Fecha a aba da empresa afim de que possa abrir outra
                await CloseOnePage(pageEmpresa)
            } catch (error) {
                console.log(error)
            }
        }
        
        console.log(`[Final-Loguin] - Todos os dados deste loguin processados, fechando navegador.`)
        await browser.close()
    } catch (error) {
        console.log(error)
    }
}

module.exports = MainNfseGoiania