const GetIntegrattionCompanies = require('./GetIntegrattionCompanies')
const GetIntegrattionLayouts = require('./GetIntegrattionLayouts')

class UnionIntegrattionLayoutsAndCompanie{
    constructor(filter={}){
        this.filter = filter
        this.getIntegrattionCompanies = new GetIntegrattionCompanies(this.filter)
        this.integrattion_companies = []
        this.integrattion_layouts = []
    }

    async getNamesSystem(idLayout){
        const getIntegrattionLayouts = new GetIntegrattionLayouts({ _id: idLayout })
        const integrattionLayout = await getIntegrattionLayouts.getData()
        let system = ''
        try {
            system = await integrattionLayout[0].system
        } catch (error) {
            system = ''
        }
        return system
    }

    async process(){
        this.integrattion_companies = await this.getIntegrattionCompanies.getData()

        try {
            const accountPaid = this.integrattion_companies[0].accountPaid

            let system = ''
            for(let layoutAccountPaid of accountPaid.layouts){
                system += `${await this.getNamesSystem(layoutAccountPaid.idLayout)}, `
            }
            system = system.substring(0, system.length - 2)
            return { system }
        } catch (error) {
            return { system: '' }
        }
    }
}
module.exports = UnionIntegrattionLayoutsAndCompanie

// const unionIntegrattionLayoutsAndCompanie = new UnionIntegrattionLayoutsAndCompanie({codi_emp: 5})
// async function process(){
//     const getdata = await unionIntegrattionLayoutsAndCompanie.process()
//     console.log(getdata)
// }
// process()