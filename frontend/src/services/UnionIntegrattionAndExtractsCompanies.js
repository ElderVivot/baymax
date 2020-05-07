const util = require('../utils/util')
const settingsCompanies = require('../utils/settingsCompanies')
const GetExtractsCompanies = require('./GetExtractsCompanies')
const UnionIntegrattionLayoutsAndCompanie = require('./UnionIntegrattionLayoutsAndCompanie')
const StatusIntegrattionOfCompanie = require('./StatusIntegrattionOfCompanie')
const IsIntegrattionLayoutCompanieOld = require('./IsIntegrattionLayoutCompanieOld')

class UnionIntegrattionAndExtractsCompanies{
    constructor(){
        this.getExtractsCompanies = new GetExtractsCompanies()
        this.extract_companies = []
        this.dataIntegrattionAndExtractsCompanies = []
    }

    async process(){
        this.extract_companies = await this.getExtractsCompanies.getData()

        for( let companie of this.extract_companies ) {
            const unionIntegrattionLayoutsAndCompanie = new UnionIntegrattionLayoutsAndCompanie({codi_emp: companie.codi_emp})
            const integrattionLayoutsAndCompanie = await unionIntegrattionLayoutsAndCompanie.process()

            let dataIntegrattionAndExtractsCompanies = {
                codi_emp: companie.codi_emp,
                nome_emp: companie.nome_emp,
                cgce_emp: settingsCompanies.formatCgceEmp(companie.tins_emp, companie.cgce_emp),
                stat_emp: settingsCompanies.statEmp(companie.stat_emp),
                regime_emp: settingsCompanies.regimeEmp(companie.regime_emp),
                regime_caixa_emp: settingsCompanies.regimeCaixaEmp(companie.regime_caixa_emp),
                dcad_emp: util.transformToDate(companie.dcad_emp),
                dina_emp: util.transformToDate(companie.dina_emp),
                telefone_emp: `${companie.dddf_emp}-${companie.fone_emp}`,
                email_emp: companie.email_emp,
                isCompanyBranch: settingsCompanies.isCompanyBranch(companie.tins_emp, companie.cgce_emp),
                layoutsAccountPaid: integrattionLayoutsAndCompanie.system,
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

            const statusIntegrattionOfCompanie = new StatusIntegrattionOfCompanie(dataIntegrattionAndExtractsCompanies)
            dataIntegrattionAndExtractsCompanies.statusAccountPaid = statusIntegrattionOfCompanie.identifiesTheStatus()
            
            if(dataIntegrattionAndExtractsCompanies.layoutsAccountPaid === "" || dataIntegrattionAndExtractsCompanies.layoutsAccountPaid === undefined){
                const isIntegrattionLayoutCompanieOld = new IsIntegrattionLayoutCompanieOld(companie)
                if(isIntegrattionLayoutCompanieOld.process() === true){
                    dataIntegrattionAndExtractsCompanies.layoutsAccountPaid = companie.layoutsAccountPaidOld
                    dataIntegrattionAndExtractsCompanies.dateAccountPaid = companie.dateAccountPaidOld
                    dataIntegrattionAndExtractsCompanies.obsAccountPaid = companie.obsAccountPaidOld
                    dataIntegrattionAndExtractsCompanies.responsibleFinancialClient = companie.responsibleFinancialClientOld
                }
            }

            this.dataIntegrattionAndExtractsCompanies.push(dataIntegrattionAndExtractsCompanies)
        }
        return this.dataIntegrattionAndExtractsCompanies
    }
}
module.exports = UnionIntegrattionAndExtractsCompanies

// const unionIntegrattionAndExtractsCompanies = new UnionIntegrattionAndExtractsCompanies()
// async function process(){
//     const getdata = await unionIntegrattionAndExtractsCompanies.process()
//     console.log(getdata)
// }
// process()