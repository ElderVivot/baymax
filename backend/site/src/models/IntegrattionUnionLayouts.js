const mongoose = require('mongoose')

// cria como se fosse a tabela do banco de dados este UserSchema
const IntegrattionUnionLayoutsSchema = new mongoose.Schema({
    codi_emp: Number,
    layouts: [{
        idLayout: String
    }],
    relationship: [{
        
    }]
})

// cria a 'tabela' de fato
module.exports = mongoose.model('integrattion_union_layouts', IntegrattionUnionLayoutsSchema, 'IntegrattionUnionLayouts')