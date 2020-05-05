const ExtractCompaniesMovements = require('../models/ExtractCompaniesMovements')

module.exports = {
    async index(req, res){
        let extractCompaniesMovements

        let queries = req.query

        if(queries === {}){
            extractCompaniesMovements = await ExtractCompaniesMovements.find({})
        } else{
            extractCompaniesMovements = await ExtractCompaniesMovements.find({...req.query})
        }

        console.log(` - ExtractCompaniesMovementsController.index`)

        return res.json(extractCompaniesMovements)
    },
}