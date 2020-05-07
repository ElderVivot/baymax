const { api } = require('./api')
const util = require('../utils/util')

class GetCompaniesSettings{
    constructor(filter={}){
        this.companies_settings = []
        this.filter = filter
        this.url = util.implementsFilterInURL('/companies_settings', this.filter)
    }

    async getData(){
        try {
            const responseCompaniesSettings = await api.get(this.url)
            if(responseCompaniesSettings.statusText === "OK"){
                this.companies_settings = responseCompaniesSettings.data
            }
        } catch (error) {
            console.log(error)
        }
        return this.companies_settings
    }
}
module.exports = GetCompaniesSettings

// const getExtractsMovements = new GetCompaniesSettings({codi_emp: 1})
// async function process(){
//     const getdata = await getExtractsMovements.getData()
//     console.log(getdata)
// }
// process()