const mongoose = require('mongoose')

// cria como se fosse a tabela do banco de dados este UserSchema
const IntegrattionLayoutSchema = new mongoose.Schema({
    system: String,
    fileType: String,
    layoutType: String,
    header: [{
        nameField: String
    }],
    fields: [{
        nameField: String,
        positionInFile: Number,
        positionInFileEnd: Number,
        nameColumn: String,
        formatDate: String
    }]
})

// cria a 'tabela' de fato
module.exports = mongoose.model('integrattion_layouts', IntegrattionLayoutSchema, 'IntegrattionLayouts')