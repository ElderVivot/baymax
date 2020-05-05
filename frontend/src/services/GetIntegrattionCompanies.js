const { api } = require('./api')

class GetIntegrattionCompanies{
    constructor(filter={}){
        this.integrattion_companies = []
        this.filter = filter
    }

    async getData(){
        try {
            const responseIntegrattionCompanies = await api.get(`/integrattion_companies`)
            if(responseIntegrattionCompanies.statusText === "OK"){
                this.integrattion_companies = responseIntegrattionCompanies.data
            }
        } catch (error) {
            console.log(error)
        }
        return this.integrattion_companies
    }
}
module.exports = GetIntegrattionCompanies