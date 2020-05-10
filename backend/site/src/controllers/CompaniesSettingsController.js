const CompaniesSettings = require('../models/CompaniesSettings')
const ExtractCompanies = require('../models/ExtractCompanies')

module.exports = {
    async index(req, res){
        const companiesSettings = await ExtractCompanies.aggregate([
            // {
            //     "$match": {"codi_emp": 5}
            // },
            {
                "$lookup": {
                    "from": "CompaniesSettings",
                    "localField": "codi_emp",
                    "foreignField": "codi_emp",
                    "as": "companiesSettings"
                }
            }, 
            // {
            //     "$unwind": { "path": "$companiesSettings", "preserveNullAndEmptyArrays": true }
            // },
            {
                "$lookup": {
                    "from": "IntegrattionCompanies",
                    "localField": "codi_emp",
                    "foreignField": "codi_emp",
                    "as": "integrattionCompanies"
                }
            },
            {
                "$lookup": {
                    "from": "IntegrattionLayouts",
                    "localField": "integrattionCompanies.0.accountPaid.layouts.0.idLayout",
                    "foreignField": "_id",
                    "as": "integrattionLayouts"
                }
            }
        ])

        console.log(` - CompaniesSettingsController.index`)

        return res.json(companiesSettings)
    },

    async show(req, res) {
        const { codi_emp } = req.params

        try {
            const companiesSettings = await CompaniesSettings.findOne( { codi_emp } )

            console.log(` - CompaniesSettingsController.show --> ${ codi_emp }`)

            return res.json(companiesSettings)
        } catch (error) {
            return res.status(400).json({error: 'Não foi possível mostrar os dados'})
        } 
    },

    async store(req, res) {
        const companiesSettings = await CompaniesSettings.create({
            ...req.body
        })

        console.log(` - CompaniesSettingsController.store --> ${req.body.codi_emp}`)

        return res.json(companiesSettings)
    },

    async update(req, res) {
        const { codi_emp } = req.params

        try {
            const companiesSettings = await CompaniesSettings.findOneAndUpdate( { codi_emp }, {
                ...req.body
            })

            console.log(` - CompaniesSettingsController.update --> ${codi_emp}`)
    
            return res.json(companiesSettings)
        } catch (error) {
            console.log(error)
            return res.status(400).json({error: 'Não foi possível atualizar os dados'})        
        }        
    },
}