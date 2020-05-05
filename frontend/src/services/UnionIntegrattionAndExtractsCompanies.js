const { api } = require('./api')

const util = require('../utils/util')
const settingsCompanies = require('../utils/settingsCompanies')
const GetExtractsCompanies = require('./GetExtractsCompanies')

class UnionIntegrattionAndExtractsCompanies{
    constructor(){
        this.getExtractsCompanies = new GetExtractsCompanies()
        this.extract_companies = []
        // this.integrattion_companies = []
        // this.integrattion_layouts = []
        this.dataIntegrattionAndExtractsCompanies = []
    }
    
    async process(){
        this.extract_companies = await this.getExtractsCompanies.getData()
        // this.integrattion_companies = this.data[1]
        // this.integrattion_layouts = this.data[2]

        this.extract_companies.map( companie => (
            this.dataIntegrattionAndExtractsCompanies.push({
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
                // layoutsAccountPaid: this.returnDataLayoutAccountPaid(companie.codi_emp).system,
                nome_municipio_emp: companie.nome_municipio_emp,
                esta_emp: companie.esta_emp,
                ramo_emp: companie.ramo_emp
            })
        ))
        return this.dataIntegrattionAndExtractsCompanies
    }

    // returnDataLayoutAccountPaid(codi_emp){
    //     let accountPaid = {}
    //     try {
    //         accountPaid = this.integrattion_companies.filter( companie => companie.codi_emp === codi_emp )[0].accountPaid
    //     } catch (error) {
    //         accountPaid = {}
    //     }
        
    //     let system = ''
    //     try {
    //         for(let layoutAccountPaid of accountPaid.layouts){
    //             system += `${this.integrattion_layouts.filter( layout => layout._id === layoutAccountPaid.idLayout )[0].system}, `
    //         }
    //         system = system.substring(0, system.length - 2)
    //         return {system}
    //     } catch (error) {
    //         return {system: ''}
    //     }
    // }
}
module.exports = UnionIntegrattionAndExtractsCompanies

// const unionIntegrattionAndExtractsCompanies = new UnionIntegrattionAndExtractsCompanies()
// async function process(){
//     const getdata = await unionIntegrattionAndExtractsCompanies.process()
//     console.log(getdata)
// }
// process()