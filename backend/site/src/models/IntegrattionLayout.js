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
        formatDate: String,
        splitField: String,
        positionFieldInTheSplit: Number,
        positionFieldInTheSplitEnd: Number,
        informationIsOnOneLineBelowTheMain: Boolean
    }],
    validationLineToPrint: [{
        nameField: String,
        typeValidation: String,
        valueValidation: String
    }],
    linesOfFile: [{
        // _id: new mongoose.Types.ObjectId(),
        nameOfLine: String,
        validations: [{
            positionInFile: Number,
            positionInFileEnd: Number,
            typeValidation: String,
            valueValidation: String,
            nextValidationOrAnd: String
        }]        
    }]
})

// cria a 'tabela' de fato
module.exports = mongoose.model('integrattion_layouts', IntegrattionLayoutSchema, 'IntegrattionLayouts')