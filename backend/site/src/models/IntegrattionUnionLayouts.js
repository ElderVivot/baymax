const mongoose = require('mongoose')

// cria como se fosse a tabela do banco de dados este UserSchema
const IntegrattionUnionLayoutsSchema = new mongoose.Schema({
    codi_emp: Number,
    layouts: [{
        idLayout: mongoose.Schema.Types.ObjectId
    }],
    relationship: [{
        idLayoutOne: mongoose.Schema.Types.ObjectId,
        fieldLayoutOne: String,
        idLayoutTwo: mongoose.Schema.Types.ObjectId,
        fieldLayoutTwo: String,
        typeComparation: String
    }]
})

// cria a 'tabela' de fato
module.exports = mongoose.model('integrattion_union_layouts', IntegrattionUnionLayoutsSchema, 'IntegrattionUnionLayouts')