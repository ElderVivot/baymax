const mongoose = require('mongoose')

// cria como se fosse a tabela do banco de dados este UserSchema
const SchemaCollection = new mongoose.Schema({
    codi_emp: Number,
    nome_emp: String,
    cgce_emp: String,
    stat_emp: String,
    regime_emp: String,
    regime_caixa_emp: String,
    dcad_emp: String,
    dina_emp: String,
    qtd_fiais_e_matriz: Number,
    telefoneAccountPaid: String,
    emailAccountPaid: String,
    statusAccountPaid: String,
    isCompanyBranch: String,
    layoutsAccountPaid: String,
    layoutsAccountPaidNewModel: String,
    dateAccountPaid: String,
    obsAccountPaid: String,
    responsibleFinancialClient: String,
    analystReceivedTraining: String,
    dateReceivedTraining: String,
    nome_municipio_emp: String,
    esta_emp: String,
    ramo_emp: String,
    fiscalTeam: String,
    accountingTeam: String,
    qtdEntryNotes: Number,
    qtdOutputNotes: Number,
    qtdServiceNotes: Number,
    qtdLancManual: Number,
    qtdLancImported: Number,
    groupCompanie: String
})

// cria a 'tabela' de fato
module.exports = mongoose.model('companies_settings_view', SchemaCollection, 'CompaniesSettingsView')