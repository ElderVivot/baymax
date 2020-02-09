const IntegrattionLayout = require('../models/IntegrattionLayout')

module.exports = {
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
    }
}