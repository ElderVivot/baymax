const IntegrattionCompanies = require('../models/IntegrattionCompanies')

module.exports = {
    async index(req, res){
        try {
            let integrattionCompanies

            let queries = req.query

            if(queries === {}){
                integrattionCompanies = await IntegrattionCompanies.find({})
            } else{
                integrattionCompanies = await IntegrattionCompanies.find({...req.query})
            }

            console.log(` - IntegrattionCompaniesController.index`)

            return res.json(integrattionCompanies)
        } catch (error) {
            console.log(error)
            return res.status(400).json({error: 'Não foi possível buscar os dados'})  
        }
    },

    async store(req, res) {
        try {
            const integrattionCompanies = await IntegrattionCompanies.create({
                ...req.body
            })
    
            console.log(` - IntegrattionCompaniesController.store --> ${JSON.stringify(req.body)}`)
    
            return res.json(integrattionCompanies)
        } catch (error) {
            console.log(error)
            return res.status(400).json({error: 'Não foi possível cadastrar os dados'})  
        }
    },

    async update(req, res) {
        const _id = req.params.id

        try {
            const integrattionCompanies = await IntegrattionCompanies.findByIdAndUpdate( {_id}, {
                ...req.body
            })

            console.log(` - IntegrattionCompaniesController.update --> ${JSON.stringify(req.body)}`)
    
            return res.json(integrattionCompanies)
        } catch (error) {
            console.log(error)
            return res.status(400).json({error: 'Não foi possível atualizar os dados'})        
        }        
    },

    async show(req, res) {
        const _id = req.params.id

        try {
            const integrattionCompanies = await IntegrattionCompanies.findOne( {_id} )

            console.log(` - IntegrattionCompaniesController.show --> ${_id}`)

            return res.json(integrattionCompanies)
        } catch (error) {
            return res.status(400).json({error: 'Não foi possível mostrar os dados'})
        } 
    },

    async delete(req, res) {
        const _id = req.params.id

        try {
            const integrattionCompanies = await IntegrattionCompanies.findByIdAndDelete( { _id })

            console.log(` - IntegrattionCompaniesController.delete --> ${_id}`)

            return res.json(integrattionCompanies)
        } catch (error) {
            return res.status(400).json({error: 'Não foi possível deletar os dados'})
        } 
    }
}