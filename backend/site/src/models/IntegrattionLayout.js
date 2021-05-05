const mongoose = require('mongoose')

// cria como se fosse a tabela do banco de dados este UserSchema
const IntegrattionLayoutSchema = new mongoose.Schema({
    system: String,
    fileType: String,
    splitFile: String,
    layoutType: String,
    header: [{
        nameColumn: String
    }],
    fields: [{
        nameField: {
            value: String,
            label: String
        },
        positionInFile: Number,
        positionInFileEnd: Number,
        nameColumn: String,
        formatDate: String,
        splitField: String,
        positionFieldInTheSplit: Number,
        positionFieldInTheSplitEnd: Number,
        sumInterestFineAndDiscount: Boolean,
        calcDifferencePaidOriginalAsInterestDiscount: Boolean,
        validateIfCnpjOrCpfIsValid: Boolean,
        multiplePerLessOne: Boolean,
        groupingField: Boolean,
        considerToCheckIfTtIsDuplicated: Boolean,
        lineThatTheDataIs: String
    }],
    validationLineToPrint: [{
        nameField: String,
        typeValidation: String,
        valueValidation: String,
        nextValidationOrAnd: String
    }],
    linesOfFile: [{
        nameOfLine: {
            value: String,
            label: String
        },
        informationIsOnOneLineBelowTheMain: Boolean,
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