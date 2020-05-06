const mongoose = require('mongoose')

// cria como se fosse a tabela do banco de dados este UserSchema
const ExtractCompaniesSchema = new mongoose.Schema({
    codi_emp: Number,
    apel_emp: String,
    razao_emp: String,
    cgce_emp: String,
    tins_emp: Number,
    stat_emp: String,
    dcad_emp: String,
    dina_emp: String,
    dtinicio_emp: String,
    dddf_emp: Number,
    fone_emp: String,
    email_emp: String,
    i_cnae20: String,
    ramo_emp: String,
    rleg_emp: String,
    dini: String,
    dfin: String,
    entradas: Number,
    saidas: Number,
    servidos: Number,
    lan_importado: Number,
    lan_manual: Number,
    grupos_contabil: String,
    grupos_fiscal: String,
    groupCompanie: String
})

// cria a 'tabela' de fato
module.exports = mongoose.model('extract_companies', ExtractCompaniesSchema, 'ExtractCompanies')