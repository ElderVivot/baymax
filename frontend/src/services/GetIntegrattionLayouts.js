const { api } = require('./api')
const util = require('../utils/util')

class GetIntegrattionLayouts{
    constructor(filter={}){
        this.integrattion_layouts = []
        this.filter = filter
        this.url = util.implementsFilterInURL('/integrattion_layouts', this.filter)
    }

    async getData(){
        try {
            const responseLayouts = await api.get(this.url)
            if(responseLayouts.statusText === "OK"){
                this.integrattion_layouts = responseLayouts.data
            }
        } catch (error) {
            console.log(error)
        }
        return this.integrattion_layouts
    }
}
module.exports = GetIntegrattionLayouts