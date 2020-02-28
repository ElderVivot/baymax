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
        self._groupingFields = {} # este obj irá gravar todos os campos que são agrupadores, linhas onde for partidas multiplas e será um lançamento só, e o que une elas é este campo
        self._validationFields = []

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
            
            numberField = funcoesUteis.analyzeIfFieldIsValid(settingField, 'numberField', -1)

            nameField = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValid(settingField, 'nameField'))
            nameField = None if nameField == "" else nameField

            valueDefault = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValid(settingField, 'valueDefault'))

            # --- este agrupamento é pra fazer a leitura de quando for um registro com vários débito pra vários créditos
            groupingField = funcoesUteis.analyzeIfFieldIsValid(settingField, 'groupingField', False)
            if groupingField is True:
                self._groupingFields[key] = True

            validationField = funcoesUteis.analyzeIfFieldIsValid(settingField, 'validationField', None)
            if validationField is not None:
                self._validationFields.append({
                    key: validationField
                })
            
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
                valueField = None if numberField == -1 and nameField is None else valueField

                if valueField is not None:
                    validField = True
            elif key.lower().find('amount') >= 0:
                valueField = funcoesUteis.treatDecimalFieldInVector(data, numberField, positionsOfHeader, nameField)
                valueField = 0 if numberField == -1 and nameField is None else valueField

                if valueField != 0:
                    validField = True
            elif key.lower().find('bank') >= 0:
                valueField = funcoesUteis.treatTextFieldInVector(data, numberField, positionsOfHeader, nameField).replace('-', ' ')
                valueField = "" if numberField == -1 and nameField is None else valueField

                if valueField != "" and valueField is not None:
                    validField = True
            else:
                splitField = funcoesUteis.analyzeIfFieldIsValid(settingField, 'splitField')

                valueField = funcoesUteis.treatTextFieldInVector(data, numberField, positionsOfHeader, nameField)
                valueField = "" if numberField == -1 and nameField is None else valueField

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

    def handleLayoutIsPartidaMultipla(self, currentLine, valuesOfFile):
        previousLine = funcoesUteis.analyzeIfFieldIsValidMatrix(valuesOfFile, -1, {}, True)
        numberLote = funcoesUteis.analyzeIfFieldIsValid(previousLine, "numberLote", 0)

        # se não houver campos agrupadores de informações cada registro será um lote sequencial
        if len(self._groupingFields) == 0:
            numberLote += 1
            return numberLote
        
        currentField = ""
        for nameField, valueField in currentLine.items():
            if funcoesUteis.analyzeIfFieldIsValid(self._groupingFields, nameField, False) is True:
                currentField = currentField + "-" + funcoesUteis.treatTextField(valueField)

        previousField = ""
        for nameField, valueField in previousLine.items():
            if funcoesUteis.analyzeIfFieldIsValid(self._groupingFields, nameField, False) is True:
                previousField = previousField + "-" + funcoesUteis.treatTextField(valueField)

        if currentField == previousField:
            return numberLote
        else:
            numberLote += 1
            return numberLote

    # esta função vai filtrar apenas as linhas que possuem o requisito válido pra ser impresso, ou seja, pra gerar a informação
    def isValidLineToPrint(self, data):
        # se não tiver nenhuma validação pra verificar já retorna true
        if len(self._validationFields) == 0:
            return True

        countFieldsValid = 0
        for validations in self._validationFields:
            for nameField, validationField in validations.items():
                valueFieldData = funcoesUteis.analyzeIfFieldIsValid(data, nameField)
                
                isEqual = funcoesUteis.analyzeIfFieldIsValid(validationField, "isEqual", None)

                if isEqual is not None and isEqual == valueFieldData:
                    countFieldsValid += 1

        if countFieldsValid == len(self._validationFields):
            return True

    #  esta função soma o total pago por cada lote, afim de comparar com os extratos bancários posteriormente
    def sumAmountPaidPerLote(self, valuesOfFile):
        amountPaidPerLote = {}
        valuesOfFileWithAmountPaid = []

        for key, currentLine in enumerate(valuesOfFile):
            previousLine = funcoesUteis.analyzeIfFieldIsValidMatrix(valuesOfFile, key-1, {}, True)
            previousNumberLote = funcoesUteis.analyzeIfFieldIsValid(previousLine, "numberLote")

            currentNumberLote = funcoesUteis.analyzeIfFieldIsValid(currentLine, "numberLote")
            amountPaid = funcoesUteis.analyzeIfFieldIsValid(currentLine, "amountPaid")

            if previousNumberLote == currentNumberLote:
                amountPaidPerLote[currentNumberLote] += amountPaid
            else:
                amountPaidPerLote[currentNumberLote] = amountPaid

        for data in valuesOfFile:
            numberLote = funcoesUteis.analyzeIfFieldIsValid(data, "numberLote")
            data['amountPaidPerLote'] = round(amountPaidPerLote[numberLote], 2)
            valuesOfFileWithAmountPaid.append(data)

        return valuesOfFileWithAmountPaid

    def process(self, file):
        # a cada processamento de um novo arquivo limpa os dados que ficam armazenados
        self._fieldsRowNotMain.clear()
        self._groupingFields.clear()
        self._validationFields = []
        posionsOfHeaderTemp = {}
        posionsOfHeader = {}

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
                        isValid = self.isValidLineToPrint(valuesOfLine)
                        if isValid is True:
                            if layoutType == 'account_paid':
                                valuesOfLine['numberLote'] = self.handleLayoutIsPartidaMultipla(valuesOfLine, valuesOfFilePayments)
                                valuesOfFilePayments.append(valuesOfLine.copy())
                            elif layoutType == 'extract_bank':
                                valuesOfFileExtracts.append(valuesOfLine.copy())

                except Exception as e:
                    print(e)
                    
        # soma o total pago por lote
        valuesOfFilePayments = self.sumAmountPaidPerLote(valuesOfFilePayments)

        return [valuesOfFilePayments, valuesOfFileExtracts]

    def processAll(self):
        for root, dirs, files in os.walk(self._wayOriginalToRead):
            for file in files:
                wayFile = os.path.join(root, file)

                if file.lower().endswith(('.xls', '.xlsx')):
                    process = self.process(wayFile)
                    self._payments.append(process[0])
                    self._extracts.append(process[1])

        return [funcoesUteis.removeAnArrayFromWithinAnother(self._payments), funcoesUteis.removeAnArrayFromWithinAnother(self._extracts)]



if __name__ == "__main__":

    from dao.src.GetSettingsCompany import GetSettingsCompany

    getSettingsCompany = GetSettingsCompany(1428)
    settings = getSettingsCompany.getSettingsFinancy()

    readFiles = ReadGeneral(1428, "C:/integracao_contabil/1428/arquivos_originais", settings)
    print(readFiles.processAll()[0])

