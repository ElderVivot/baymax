const mongoose = require('mongoose')

// cria como se fosse a tabela do banco de dados este UserSchema
const IntegrattionCompaniesSchema = new mongoose.Schema({
    codi_emp: Number,
    accountPaid: {
        isReliable: Boolean,
        layouts: [{
            idLayout: mongoose.Schema.Types.ObjectId
        }]
    }
})

// cria a 'tabela' de fato
module.exports = mongoose.model('integrattion_companies', IntegrattionCompaniesSchema, 'IntegrattionCompanies')