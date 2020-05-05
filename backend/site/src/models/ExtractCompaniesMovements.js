const mongoose = require('mongoose')

// cria como se fosse a tabela do banco de dados este UserSchema
const ExtractCompaniesMovementsSchema = new mongoose.Schema({
    codi_emp: Number,
    dini: String,
    dfin: String,
    entradas: Number,
    saidas: Number,
    servidos: Number,
    lan_importado: Number,
    lan_manual: Number,
    grupos_contabil: String,
    grupos_fiscal: String
})

// cria a 'tabela' de fato
module.exports = mongoose.model('extract_companies_movements', ExtractCompaniesMovementsSchema, 'ExtractCompaniesMovements')