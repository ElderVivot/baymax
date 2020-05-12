const { api } = require('./api')
const settingsColumns = require('../pages/CompaniesSettings/SettingsColumns')

class PostCompaniesSettings{
    constructor(companieSetting=[]){
        this.companieSetting = companieSetting
    }

    async postData(){
        try {
            const dataCompanie = this.getColumnsIsNecessary(this.companieSetting)
            let companieAlreadyExist = false
            
            const findCompanie = await api.get(`/companies_settings/${dataCompanie['codi_emp']}`)
            if(findCompanie.statusText === "OK"){
                if(findCompanie.data !== null){
                    companieAlreadyExist = true
                }
            }

            if(companieAlreadyExist === true){
                await api.put(`/companies_settings/${dataCompanie['codi_emp']}`, { ...dataCompanie })
            } else {
                await api.post('/companies_settings', { ...dataCompanie })
            }
        } catch (error) {
            console.log(error)
        }
    }

    getColumnsIsNecessary(companieSetting={}){
        try {
            let dataCompanie = {}
            for(let i=0; i < companieSetting.length; i++){
                try {
                    const nameField = settingsColumns[i].data
                    const readOnly = settingsColumns[i].readOnly      
                    if(readOnly === undefined || readOnly === false || nameField === "codi_emp"){
                        if(companieSetting[i] === null){
                            companieSetting[i] = ""
                        }
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
}
module.exports = PostCompaniesSettings

// const getExtractsMovements = new GetCompaniesSettings({codi_emp: 1})
// async function process(){
//     const getdata = await getExtractsMovements.getData()
//     console.log(getdata)
// }
// process()