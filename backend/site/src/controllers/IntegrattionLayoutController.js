const IntegrattionLayout = require('../models/IntegrattionLayout')

module.exports = {
    async index(req, res){
        const integrattionLayout = await IntegrattionLayout.find({})

        return res.json(integrattionLayout)
    },

    async store(req, res) {
        // desestruturação --> busco um campo dentro de um JSON passando só o nome dele dentro de chaves
        const { system, fileType, layoutType, header, fields } = req.body

        const integrattionLayout = await IntegrattionLayout.create({
            system,
            fileType,
            layoutType,
            header,
            fields
        })

        return res.json(integrattionLayout)
    },

    async update(req, res) {
        const _id = req.params.id

        // desestruturação --> busco um campo dentro de um JSON passando só o nome dele dentro de chaves
        const { system, fileType, layoutType, header, fields } = req.body

        const integrattionLayout = await IntegrattionLayout.updateOne( {_id}, {
            system,
            fileType,
            layoutType,
            header,
            fields
        })

        return res.json(integrattionLayout)
    },

    async show(req, res) {
        const _id = req.params.id

        const integrattionLayout = await IntegrattionLayout.findOne( {_id} )

        return res.json(integrattionLayout)
    }
}