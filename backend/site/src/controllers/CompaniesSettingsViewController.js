const CompaniesSettingsView = require('../models/CompaniesSettingsView')

module.exports = {
    async store(req, res) {
        try {
            const companiesSettingsView = await CompaniesSettingsView.insertMany( req.body )
    
            console.log(` - CompaniesSettingsViewController.store`)
    
            return res.json(companiesSettingsView)
        } catch (error) {
            console.log(error)
            return res.status(400).json({error: 'Não foi possível inserir os dados'})
        }
        
    },

    async destroy(req, res) {

        try {
            const companiesSettingsView = await CompaniesSettingsView.deleteMany( { })

            console.log(` - CompaniesSettingsController.destroy`)
    
            return res.json(companiesSettingsView)
        } catch (error) {
            console.log(error)
            return res.status(400).json({error: 'Não foi possível deletar os dados'})        
        }        
    },
}