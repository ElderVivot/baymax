const IntegrattionCompanies = require('../models/IntegrattionCompanies')

module.exports = {
    async index(req, res){
        let integrattionCompanies

        let queries = req.query

        if(queries === {}){
            integrattionCompanies = await IntegrattionCompanies.find({})
        } else{
            integrattionCompanies = await IntegrattionCompanies.find({...req.query})
        }

        console.log(` - IntegrattionCompaniesController.index`)

        return res.json(integrattionCompanies)
    },

    async store(req, res) {
        const { codi_emp, accountPaid } = req.body

        const integrattionCompanies = await IntegrattionCompanies.create({
            codi_emp,
            accountPaid
        })

        console.log(` - IntegrattionCompaniesController.store --> ${codi_emp}`)

        return res.json(integrattionCompanies)
    },

    async update(req, res) {
        const _id = req.params.id

        const { codi_emp, accountPaid } = req.body

        try {
            const integrattionCompanies = await IntegrattionCompanies.findByIdAndUpdate( {_id}, {
                codi_emp,
                accountPaid
            })

            console.log(` - IntegrattionCompaniesController.update --> ${codi_emp}`)
    
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