import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import json
from tools.leArquivos import leXls_Xlsx, leTxt, readJson
import tools.funcoesUteis as funcoesUteis


class ReadGeneral(object):

    def __init__(self, codiEmp, wayOriginalToRead, settings):
        self._codiEmp = codiEmp
        self._wayOriginalToRead = wayOriginalToRead
        self._settings = settings
        self._payments = []
        self._extracts = []
        self._fieldsRowNotMain = {}

    def identifiesTheHeader(self, data, settingLayout):
        posionsOfHeader = {}
        header = funcoesUteis.analyzeIfFieldIsValid(settingLayout, 'header')
        dataManipulate = []

        if len(header) == 0:
            return None
        
        for field in data:
            dataManipulate.append(funcoesUteis.treatTextField(field))
        
        countNumberHeader = 0
        for field in header:
            nameField = funcoesUteis.treatTextField(field['nameField'])

            if dataManipulate.count(nameField) > 0:
                countNumberHeader += 1

        if countNumberHeader == len(header):
            for keyField, nameField in enumerate(dataManipulate):
                if nameField != "":
                    posionsOfHeader[nameField] = keyField

        return posionsOfHeader

    def identifiesIfTheRowCorrect(self, row, data):
        if len(row) == 0:
            return None

        countHeaderEquals = 0

        for rowValidation in row:
            numberField = funcoesUteis.analyzeIfFieldIsValid(rowValidation, 'numberField')
            validation = funcoesUteis.analyzeIfFieldIsValid(rowValidation, 'validation')
            value = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValid(rowValidation, 'value'))

            if validation == "isDate":
                valueField = funcoesUteis.treatTextFieldInVector(data, numberField)
                valueFieldDate = funcoesUteis.retornaCampoComoData(valueField) if len(valueField) <= 10 else None # este campo é pra caso tenha algum valor que seja data + horário ele não cai na verificação do isDate
                if valueFieldDate is not None:
                    countHeaderEquals += 1
            elif validation == "isEqual":
                valueField = funcoesUteis.treatTextFieldInVector(data, numberField)
                if valueField == value:
                    countHeaderEquals += 1
        
        if countHeaderEquals == len(row):
            return True

    def treatDataLayout(self, data, settingFields, positionsOfHeader):
        valuesOfLine = {}

        for key, settingField in settingFields.items():
            numberField = funcoesUteis.analyzeIfFieldIsValid(settingField, 'numberField')
            nameField = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValid(settingField, 'nameField'))
            valueDefault = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValid(settingField, 'valueDefault'))
            validField = False

            row = funcoesUteis.analyzeIfFieldIsValid(settingField, 'row')
            isRowCorrect = self.identifiesIfTheRowCorrect(row, data)
            
            rowIsMain = funcoesUteis.analyzeIfFieldIsValid(valuesOfLine, 'row')
            if rowIsMain == "" or rowIsMain == "main":
                rowIsMain = 'not_main' if isRowCorrect is True else 'main'
            
            if key.lower().find('date') >= 0:
                formatDate = funcoesUteis.analyzeIfFieldIsValid(settingField, 'formatDate')
                if formatDate == 'dd/mm/aaaa':
                    formatDate = 1
                elif formatDate == 'aaaa-mm-dd':
                    formatDate = 2
                else:
                    formatDate = 1
                
                valueField = funcoesUteis.treatDateFieldInVector(data, numberField, positionsOfHeader, nameField, formatDate, rowIsMain)

                if valueField is not None:
                    validField = True
            elif key.lower().find('amount') >= 0:
                valueField = funcoesUteis.treatDecimalFieldInVector(data, numberField, positionsOfHeader, nameField)

                if valueField != 0:
                    validField = True
            else:
                splitField = funcoesUteis.analyzeIfFieldIsValid(settingField, 'splitField')

                valueField = funcoesUteis.treatTextFieldInVector(data, numberField, positionsOfHeader, nameField)

                if splitField != "":
                    valueField = valueField.split(splitField)
                    if len(valueField) > 1:
                        valueField = ''.join(valueField[1:])
                    else:
                        valueField = ''.join(valueField[0:])
                    valueField = funcoesUteis.minimalizeSpaces(valueField)

                if valueField != "":
                    validField = True
            
            if validField is False and valueDefault != "":
                validField = True
                valueField = valueDefault

            if validField is True:
                valuesOfLine['row'] = rowIsMain
                valuesOfLine[key] = valueField                    
        
        return valuesOfLine

    def updateFieldsNotMain(self, data, settingFields):
        row = funcoesUteis.analyzeIfFieldIsValid(data, 'row')

        if row == 'not_main':
            for nameField, valueField in data.items():

                fieldIsAnotherRow = funcoesUteis.returnDataFieldInDict(settingFields, [nameField, 'row'])
                if fieldIsAnotherRow != "":
                    if nameField.lower().find('date') >= 0:
                        if valueField is not None:
                            self._fieldsRowNotMain[nameField] = valueField
                    elif nameField.lower().find('amount') >= 0:
                        if valueField != 0:
                            self._fieldsRowNotMain[nameField] = valueField
                    else:
                        if valueField != "":
                            self._fieldsRowNotMain[nameField] = valueField

    def groupsRowData(self, valuesOfLine):
        for nameField, valueField in self._fieldsRowNotMain.items():
            valuesOfLine[nameField] = valueField
        
        return valuesOfLine

    def handleExtracts(self, valuesOfLine):
        amount = funcoesUteis.treatDecimalField(funcoesUteis.analyzeIfFieldIsValid(valuesOfLine, 'amount'))
        if amount < 0:
            operation = '-'
            amount *= -1
        else:
            operation = '+'

        valuesOfLine['amount'] = amount
        valuesOfLine['operation'] = operation

        if operation == "+":
            historicCode = 24
        else:
            historicCode = 78

        valuesOfLine['historicCode'] = historicCode

        return valuesOfLine

    def process(self, file):
        self._fieldsRowNotMain.clear() # a cada processamento de um novo arquivo limpa os dados que ficam armazenados

        settingsLayouts = funcoesUteis.analyzeIfFieldIsValid( self._settings, 'settingsLayouts')

        if len(settingsLayouts) == 0:
            return None

        valuesOfLine = {}
        valuesOfFilePayments = []
        valuesOfFileExtracts = []
        posionsOfHeader = {}

        for setting in settingsLayouts:
            
            layoutType = setting['layoutType']
            if layoutType != "account_paid" and layoutType != "extract_bank":
                return None
            
            if setting['fileType'] == 'excel':
                dataFile = leXls_Xlsx(file)
            else:
                dataFile = []

            fields = setting['fields']

            for key, data in enumerate(dataFile):

                try:
                    posionsOfHeaderTemp = self.identifiesTheHeader(data, setting)
                    if posionsOfHeaderTemp is not None:
                        if len(posionsOfHeaderTemp.items()) > 0:
                            posionsOfHeader = posionsOfHeaderTemp
                            continue

                    valuesOfLine = self.treatDataLayout(data, fields, posionsOfHeader)
                    self.updateFieldsNotMain(valuesOfLine, fields)
                    valuesOfLine = self.groupsRowData(valuesOfLine)
                    
                    if layoutType == 'account_paid':
                        validationDate = funcoesUteis.analyzeIfFieldIsValid(valuesOfLine, 'paymentDate', None)
                        validationAmount = funcoesUteis.analyzeIfFieldIsValid(valuesOfLine, 'amountPaid', 0)
                        valuesOfLine['document'] = funcoesUteis.handleNote(funcoesUteis.analyzeIfFieldIsValid(valuesOfLine, 'document'))
                    elif layoutType == 'extract_bank':
                        valuesOfLine = self.handleExtracts(valuesOfLine)
                        validationDate = funcoesUteis.analyzeIfFieldIsValid(valuesOfLine, 'dateTransaction', None)
                        validationAmount = funcoesUteis.analyzeIfFieldIsValid(valuesOfLine, 'amount', 0)
                    else:
                        validationDate = None
                        validationAmount = 0
                    
                    valuesOfLine['bank'] = funcoesUteis.analyzeIfFieldIsValid(valuesOfLine, 'bank') # o banco é um campo obrigatório na ordenação do Excel. Portanto, se não existir ele vai dar erro. Por isto desta linha. 
                    
                    if validationDate is not None and validationAmount != 0:
                        if layoutType == 'account_paid':
                            valuesOfFilePayments.append(valuesOfLine.copy())
                        elif layoutType == 'extract_bank':
                            valuesOfFileExtracts.append(valuesOfLine.copy())

                except Exception as e:
                    print(e)
                    
        return [valuesOfFilePayments, valuesOfFileExtracts]

    def processAll(self):
        for root, dirs, files in os.walk(self._wayOriginalToRead):
            for file in files:
                wayFile = os.path.join(root, file)

                if file.lower().endswith(('.xls', '.xlsx')):
                    self._payments.append(self.process(wayFile)[0])
                    self._extracts.append(self.process(wayFile)[1])

        return [funcoesUteis.removeAnArrayFromWithinAnother(self._payments), funcoesUteis.removeAnArrayFromWithinAnother(self._extracts)]



# if __name__ == "__main__":

#     from dao.src.GetSettingsCompany import GetSettingsCompany

#     getSettingsCompany = GetSettingsCompany(1498)
#     settings = getSettingsCompany.getSettingsFinancy()

#     readFiles = ReadGeneral(1498, "C:/integracao_contabil/1498/arquivos_originais", settings)
#     print(readFiles.processAll()[1])

