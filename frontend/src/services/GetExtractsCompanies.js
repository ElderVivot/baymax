const { api } = require('./api')

class GetExtractsCompanies{
    constructor(filter={}){
        this.extract_companies = []
        this.filter = filter
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