const IntegrattionCompanies = require('../models/IntegrattionCompanies')

module.exports = {
    // async index(req, res){
    //     const integrattionLayout = await IntegrattionLayout.find({})

    //     console.log(` - IntegrattionLayoutController.index`)

    //     return res.json(integrattionLayout)
    // },

    async store(req, res) {
        const { codi_emp, accountPaid } = req.body

        const integrattionCompanies = await IntegrattionCompanies.create({
            codi_emp,
            accountPaid
        })

        console.log(` - IntegrattionCompaniesController.store --> ${codi_emp}`)

        return res.json(integrattionCompanies)
    },

    // async update(req, res) {
    //     const _id = req.params.id

    //     const { system, fileType, layoutType, header, fields, validationLineToPrint, linesOfFile } = req.body

    //     try {
    //         const integrattionLayout = await IntegrattionLayout.findByIdAndUpdate( {_id}, {
    //             system,
    //             fileType,
    //             layoutType,
    //             header,
    //             fields,
    //             validationLineToPrint,
    //             linesOfFile
    //         })

    //         console.log(` - IntegrattionLayoutController.update --> ${_id} - ${system}`)
    
    //         return res.json(integrattionLayout)
    //     } catch (error) {
    //         console.log(error)
    //         return res.status(400).json({error: 'Não foi possível atualizar os dados'})        
    //     }        
    // },

    // async show(req, res) {
    //     const _id = req.params.id

    //     try {
    //         const integrattionLayout = await IntegrattionLayout.findOne( {_id} )

    //         console.log(` - IntegrattionLayoutController.show --> ${_id}`)

    //         return res.json(integrattionLayout)
    //     } catch (error) {
    //         return res.status(400).json({error: 'Não foi possível mostrar os dados'})
    //     } 
    // },

    // async delete(req, res) {
    //     const _id = req.params.id

    //     try {
    //         const integrattionLayout = await IntegrattionLayout.findByIdAndDelete( { _id })

    //         console.log(` - IntegrattionLayoutController.delete --> ${_id} - ${system}`)

    //         return res.json(integrattionLayout)
    //     } catch (error) {
    //         return res.status(400).json({error: 'Não foi possível deletar os dados'})
    //     } 
    // }
}