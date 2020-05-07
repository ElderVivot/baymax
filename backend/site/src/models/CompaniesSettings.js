const mongoose = require('mongoose')

// cria como se fosse a tabela do banco de dados este UserSchema
const SchemaCollection = new mongoose.Schema({
    codi_emp: Number,
    statusAccountPaid: String,
    responsibleFinancialClient: String,
    telefoneAccountPaid: String,
    emailAccountPaid: String,
    obsAccountPaid: String,
    layoutsAccountPaid: String,
    dateAccountPaid: String,
    analystReceivedTraining: String,
    dateReceivedTraining: String
})

// cria a 'tabela' de fato
module.exports = mongoose.model('companies_settings', SchemaCollection, 'CompaniesSettings')