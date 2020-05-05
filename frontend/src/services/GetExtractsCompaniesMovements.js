const { api } = require('./api')
const util = require('../utils/util')

class GetExtractsMovements{
    constructor(filter={}){
        this.extract_companies_movements = []
        this.filter = filter
        this.url = util.implementsFilterInURL('/extract_companies_movements', this.filter)
    }

    async getData(){
        try {
            const responseExtractCompaniesMovements = await api.get(this.url)
            if(responseExtractCompaniesMovements.statusText === "OK"){
                this.extract_companies_movements = responseExtractCompaniesMovements.data
            }
        } catch (error) {
            console.log(error)
        }
        return this.extract_companies_movements
    }
}
module.exports = GetExtractsMovements

// const getExtractsMovements = new GetExtractsMovements({codi_emp: 1})
// async function process(){
//     const getdata = await getExtractsMovements.getData()
//     console.log(getdata)
// }
// process()