const moment = require('moment')
const GetExtractCompanies = require('../controllers/GetExtractCompanies')
const MainNfseGoiania = require('./MainNfseGoiania')

class Applicattion{
    constructor(){
        this.companies = []
        this.dateHourProcessing = moment().format('YYYY-MM-DD_hh-mm-ss_a')
        this.dateInicial = moment('01/05/2020', 'DD/MM/YYYY')
        this.dateFinal = moment('31/05/2020', 'DD/MM/YYYY')
    }

    async getCompaniesActive(){
        const getExtractCompanies = new GetExtractCompanies()
        const companies = await getExtractCompanies.getData()
        for(let companie of companies){
            const cgce_emp = companie['cgce_emp']
            // ignora as empresas com CNPJ inválido
            if(cgce_emp === null || cgce_emp === "" || cgce_emp === "00000000000000"){
                continue
            }

            const stat_emp = companie['stat_emp'].toUpperCase()
            const dina_emp = companie['dina_emp'] === null ? null : moment(companie['dina_emp'].substring(0,10))
            if(dina_emp !== null){
                if( dina_emp > this.dateFinal ){
                    this.companies.push(cgce_emp)
                }
            } else {
                if(stat_emp === "A"){
                    this.companies.push(cgce_emp)
                }
            }
        }
    }

    async process() {
        this.getCompaniesActive()

        const settings = { 
            dateHourProcessing: this.dateHourProcessing,
            companies: this.companies,
            loguin: '73470384134',
            password: 'soma100'
        }

        MainNfseGoiania(settings)
    }
}

applicattion = new Applicattion()
applicattion.process()