const { api } = require('./api')
const util = require('../utils/util')
const settingsColumns = require('../pages/CompaniesSettings/SettingsColumns')

class PostCompaniesSettings{
    constructor(filter={}){
        this.companies_settings = []
        this.filter = filter
        this.url = util.implementsFilterInURL('/companies_settings', this.filter)
    }

    async postData(values={}){
        try {
            await api.post(this.url, { ...values })
        } catch (error) {
            console.log('')
        }
        return this.companies_settings
    }

    getColumnsIsNecessary(companieSetting={}){
        try {
            let dataCompanie = {}
            for(let i=0; i < companieSetting.length; i++){
                try {
                    const nameField = settingsColumns[i].data
                    const readOnly = settingsColumns[i].readOnly      
                    if(readOnly === undefined || readOnly === false || nameField === "codi_emp"){
                        dataCompanie[nameField] = companieSetting[i]
                    }
                } catch (error) {
                    continue
                }
            }
            return dataCompanie
        } catch (error) {
            return {}
        }
    }

    async process(companiesSettings){
        try {
            for(let companieSetting of companiesSettings){
                const dataCompanie = this.getColumnsIsNecessary(companieSetting)
                await this.postData(dataCompanie)
            }
        } catch (error) {
            
        }
    }
}
module.exports = PostCompaniesSettings

// const getExtractsMovements = new GetCompaniesSettings({codi_emp: 1})
// async function process(){
//     const getdata = await getExtractsMovements.getData()
//     console.log(getdata)
// }
// process()