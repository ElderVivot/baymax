const ExtractCompanies = require('../models/ExtractCompanies')

module.exports = {
    async index(req, res){
        const extractCompanies = await ExtractCompanies.find()

        console.log(` - ExtractCompaniesController.index`)

        return res.json(extractCompanies)
    },
}