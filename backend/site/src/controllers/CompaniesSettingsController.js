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

        console.log(` - CompaniesSettings.index`)

        return res.json(companiesSettings)
    },

    async store(req, res) {
        // const { codi_emp, accountPaid } = req.body

        const companiesSettings = await CompaniesSettings.create({
            ...req.body
        })

        console.log(` - CompaniesSettingsController.store --> ${req.body.codi_emp}`)

        return res.json(companiesSettings)
    },

    // async update(req, res) {
    //     const _id = req.params.id

    //     const { codi_emp, accountPaid } = req.body

    //     try {
    //         const integrattionCompanies = await IntegrattionCompanies.findByIdAndUpdate( {_id}, {
    //             codi_emp,
    //             accountPaid
    //         })

    //         console.log(` - IntegrattionCompaniesController.update --> ${codi_emp}`)
    
    //         return res.json(integrattionCompanies)
    //     } catch (error) {
    //         console.log(error)
    //         return res.status(400).json({error: 'Não foi possível atualizar os dados'})        
    //     }        
    // },
}