const util = require('../utils/util')
const SettingsCompanies = require('../utils/SettingsCompanies')
const GetCompaniesSettings = require('./GetCompaniesSettings')
const StatusIntegrattionOfCompanie = require('./StatusIntegrattionOfCompanie')

class SettingsCompaniesSettings{
    constructor(){
        this.getCompaniesSettings = new GetCompaniesSettings()
        this.extract_companies = []
        this.dataSettingsCompaniesSettings = []
    }

    async process(){
        this.extract_companies = await this.getCompaniesSettings.getData()

        for( let companie of this.extract_companies ) {
            const companiesSettings = util.getDataInObjectOrArray(companie, ['companiesSettings', 0], {})
            const integrattionLayouts = util.getDataInObjectOrArray(companie, ['integrattionLayouts', 0], {})

            let dataSettingsCompaniesSettings = {
                codi_emp: companie.codi_emp,
                nome_emp: companie.nome_emp,
                cgce_emp: SettingsCompanies.formatCgceEmp(companie.tins_emp, companie.cgce_emp),
                stat_emp: SettingsCompanies.statEmp(companie.stat_emp),
                regime_emp: SettingsCompanies.regimeEmp(companie.regime_emp),
                regime_caixa_emp: SettingsCompanies.regimeCaixaEmp(companie.regime_caixa_emp),
                dcad_emp: util.transformToDate(companie.dcad_emp),
                dina_emp: util.transformToDate(companie.dina_emp),
                qtd_fiais_e_matriz: companie.qtd_fiais_e_matriz,
                telefoneAccountPaid: companiesSettings.telefoneAccountPaid || util.handleTelefone(companie.dddf_emp, companie.fone_emp),
                emailAccountPaid: companiesSettings.emailAccountPaid || companie.email_emp,
                statusAccountPaid: companiesSettings.statusAccountPaid,
                isCompanyBranch: SettingsCompanies.isCompanyBranch(companie.tins_emp, companie.cgce_emp),
                layoutsAccountPaid: companiesSettings.layoutsAccountPaid || integrattionLayouts.system || companie.layoutsAccountPaidOld,
                layoutsAccountPaidNewModel: companiesSettings.layoutsAccountPaid || integrattionLayouts.system,
                dateAccountPaid: companiesSettings.dateAccountPaid || companie.dateAccountPaidOld,
                obsAccountPaid: companiesSettings.obsAccountPaid || companie.obsAccountPaidOld,
                responsibleFinancialClient: companiesSettings.responsibleFinancialClient || companie.responsibleFinancialClientOld,
                analystReceivedTraining: companiesSettings.analystReceivedTraining,
                dateReceivedTraining: companiesSettings.dateReceivedTraining,
                nome_municipio_emp: companie.nome_municipio_emp,
                esta_emp: companie.esta_emp,
                ramo_emp: companie.ramo_emp,
                fiscalTeam: companie.grupos_fiscal,
                accountingTeam: companie.grupos_contabil,
                qtdEntryNotes: companie.entradas,
                qtdOutputNotes: companie.saidas,
                qtdServiceNotes: companie.servicos,
                qtdLancManual: companie.lan_manual,
                qtdLancImported: companie.lan_importado,
                groupCompanie: companie.groupCompanie,
                dateAccountPaidOld: companie.dateAccountPaidOld
            }

            const statusIntegrattionOfCompanie = new StatusIntegrattionOfCompanie(dataSettingsCompaniesSettings)
            const statusIdentified = statusIntegrattionOfCompanie.identifiesTheStatus()
            
            dataSettingsCompaniesSettings.statusAccountPaid = statusIdentified
            if(dataSettingsCompaniesSettings.statusAccountPaid !== "Concluída - Modelo Antigo"){
                dataSettingsCompaniesSettings.dateAccountPaid = companiesSettings.dateAccountPaid
                dataSettingsCompaniesSettings.obsAccountPaid = companiesSettings.obsAccountPaid
                dataSettingsCompaniesSettings.responsibleFinancialClient = companiesSettings.responsibleFinancialClient
            } 
            
            if(statusIdentified === "Sem Movimento") {
                dataSettingsCompaniesSettings.stat_emp = 'Sem Movimento'
            }

            if( dataSettingsCompaniesSettings.dina_emp !== "" && dataSettingsCompaniesSettings.dina_emp !== null ){
                dataSettingsCompaniesSettings.stat_emp = 'Inativa'
            }

            this.dataSettingsCompaniesSettings.push(dataSettingsCompaniesSettings)
        }
        return this.dataSettingsCompaniesSettings
    }
}
module.exports = SettingsCompaniesSettings