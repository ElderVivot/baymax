const api = require('../services/api')

class GetExtractsCompanies{
    constructor(){
        this.extract_companies = []
    }

    async getData(){
        try {
            const responseExtractCompanies = await api.get(`/extract_companies`)
            if(responseExtractCompanies.statusText === "OK"){
                this.extract_companies = responseExtractCompanies.data   
            }
        } catch (error) {
            console.log(error)
        }
        return this.extract_companies
    }
}
module.exports = GetExtractsCompanies