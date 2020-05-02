const { api } = require('./api')

const util = require('../utils/util')
const settingsCompanies = require('../utils/settingsCompanies')

class GetDataIntegrattionAndExtractsCompanies{
    constructor(){
        this.extract_companies = []
        this.integrattion_companies = []
        this.integrattion_layouts = []
    }

    async getData(){
        try {
            const responseExtractCompanies = await api.get(`/extract_companies`)
            if(responseExtractCompanies.statusText === "OK"){
                this.extract_companies = responseExtractCompanies.data   
            }

            const responseIntegrattionCompanies = await api.get(`/integrattion_companies`)
            if(responseIntegrattionCompanies.statusText === "OK"){
                this.integrattion_companies = responseIntegrattionCompanies.data
            }

            const responseLayouts = await api.get(`/integrattion_layouts`)
            if(responseLayouts.statusText === "OK"){
                this.integrattion_layouts = responseLayouts.data
            }
        } catch (error) {
            console.log(error)
        }
        return [this.extract_companies, this.integrattion_companies, this.integrattion_layouts]
    }
}

class ManipulateIntegrattionAndExtractsCompanies{
    constructor(){
        this.getDataIntegrattionAndExtractsCompanies = new GetDataIntegrattionAndExtractsCompanies()
        this.data = []
        this.extract_companies = []
        this.integrattion_companies = []
        this.integrattion_layouts = []
        this.dataIntegrattionAndExtractsCompanies = []
    }

    async process(){
        this.data = await this.getData()
        this.extract_companies = this.data[0]
        this.integrattion_companies = this.data[1]
        this.integrattion_layouts = this.data[2]

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
                layoutsAccountPaid: this.returnDataLayoutAccountPaid(companie.codi_emp).system,
                nome_municipio_emp: companie.nome_municipio_emp,
                esta_emp: companie.esta_emp,
                ramo_emp: companie.ramo_emp
            })
        ))
        return this.dataIntegrattionAndExtractsCompanies
    }

    async getData(){
        return await this.getDataIntegrattionAndExtractsCompanies.getData()
    }

    returnDataLayoutAccountPaid(codi_emp){
        let accountPaid = {}
        try {
            accountPaid = this.integrattion_companies.filter( companie => companie.codi_emp === codi_emp )[0].accountPaid
        } catch (error) {
            accountPaid = {}
        }
        
        let system = ''
        try {
            for(let layoutAccountPaid of accountPaid.layouts){
                system += `${this.integrattion_layouts.filter( layout => layout._id === layoutAccountPaid.idLayout )[0].system}, `
            }
            system = system.substring(0, system.length - 2)
            return {system}
        } catch (error) {
            return {system: ''}
        }
    }
}
module.exports.ManipulateIntegrattionAndExtractsCompanies = ManipulateIntegrattionAndExtractsCompanies

// const manipulateIntegrattionAndExtractsCompanies = new ManipulateIntegrattionAndExtractsCompanies()
// async function getData(){
//     const getdata = await manipulateIntegrattionAndExtractsCompanies.process()
//     console.log(getdata)
// }
// getData()