const mongoose = require('mongoose')

// cria como se fosse a tabela do banco de dados este UserSchema
const IntegrattionCompaniesSchema = new mongoose.Schema({
    codi_emp: Number,
    accountPaid: {
        isReliable: Boolean,
        layouts: [{
            idLayout: mongoose.Schema.Types.ObjectId,
            bankAndAccountCorrelation: [{
                bankFile: String,
                accountFile: String,
                bankNew: String,
                accountNew: String
            }],
            validateIfDataIsThisCompanie: [{
                nameField: String,
                typeValidation: String,
                valueValidation: String,
                nextValidationOrAnd: String
            }]
        }]
    },
    proofPayment: [{
        value: Number,
        label: String
    }]
})

// cria a 'tabela' de fato
module.exports = mongoose.model('integrattion_companies', IntegrattionCompaniesSchema, 'IntegrattionCompanies')