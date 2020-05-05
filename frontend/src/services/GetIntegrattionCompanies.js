const { api } = require('./api')
const util = require('../utils/util')

class GetIntegrattionCompanies{
    constructor(filter={}){
        this.integrattion_companies = []
        this.filter = filter
        this.url = util.implementsFilterInURL('/integrattion_companies', this.filter)
    }

    async getData(){
        try {
            const responseIntegrattionCompanies = await api.get(this.url)
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