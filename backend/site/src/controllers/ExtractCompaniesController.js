const ExtractCompanies = require('../models/ExtractCompanies')

module.exports = {
    async index(req, res){
        const extractCompanies = await ExtractCompanies.find({ stat_emp: 'A' })

        console.log(` - ExtractCompaniesController.index`)

        return res.json(extractCompanies)
    },
}