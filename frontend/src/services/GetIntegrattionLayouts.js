const { api } = require('./api')

class GetIntegrattionLayouts{
    constructor(filter={}){
        this.integrattion_layouts = []
        this.filter = filter
    }

    async getData(){
        try {
            const responseLayouts = await api.get(`/integrattion_layouts`)
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