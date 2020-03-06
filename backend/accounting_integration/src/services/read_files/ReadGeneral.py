import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import json
from tools.leArquivos import leXls_Xlsx, leTxt, readJson, readCsv
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
        self._validationsLineToPrint = []

    def identifiesTheHeader(self, data, settingLayout):
        # :data são os valores de cada "linha" dos arquivos processados
        # :settingLayout é a configuração do layout que está no banco de dados

        posionsOfHeader = {}
        header = funcoesUteis.analyzeIfFieldIsValid(settingLayout, 'header') # pega as configurações só do cabeçalho
        dataManipulate = []

        # se não tiver cabeçalho já retorna em branco
        if len(header) == 0:
            return None
        
        for field in data:
            dataManipulate.append(funcoesUteis.treatTextField(field))
        
        countNumberHeader = 0
        for field in header:
            nameColumn = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValid(field, 'nameColumn'))

            if dataManipulate.count(nameColumn) > 0:
                countNumberHeader += 1

        if countNumberHeader == len(header):
            for keyField, nameColumn in enumerate(dataManipulate):
                if nameColumn != "":
                    posionsOfHeader[nameColumn] = keyField

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

    #  pra saber quais campos são de agrupamento ou de validação eu não preciso saber o valor daquela linha, então não preciso identifá-los pra toda linha
    #  que é processada
    def analyzeSettingFieldsThatAreNecessaryData(self, settingFields):
        for settingField in settingFields:
            nameField = funcoesUteis.analyzeIfFieldIsValid(settingField, 'nameField')

            # --- este agrupamento é pra fazer a leitura de quando for um registro com vários débito pra vários créditos
            groupingField = funcoesUteis.analyzeIfFieldIsValid(settingField, 'groupingField', False)
            if groupingField is True:
                self._groupingFields[nameField] = True

            validationLineToPrint = funcoesUteis.analyzeIfFieldIsValid(settingField, 'validationLineToPrint', None)
            if validationLineToPrint is not None:
                objValidationLineToPrint = { nameField: validationLineToPrint }
                if self._validationsLineToPrint.count(objValidationLineToPrint) == 0:
                    self._validationsLineToPrint.append(objValidationLineToPrint)

    def treatDataLayout(self, data, settingFields, positionsOfHeader):
        valuesOfLine = {}

        for settingField in settingFields:
            nameField = funcoesUteis.analyzeIfFieldIsValid(settingField, 'nameField')

            numberField = funcoesUteis.analyzeIfFieldIsValid(settingField, 'numberField', -1)

            nameColumn = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValid(settingField, 'nameColumn'))
            nameColumn = None if nameColumn == "" else nameColumn

            valueDefault = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValid(settingField, 'valueDefault'))
            
            validField = False

            row = funcoesUteis.analyzeIfFieldIsValid(settingField, 'row')
            isRowCorrect = self.identifiesIfTheRowCorrect(row, data)
            # print(data, isRowCorrect)
            
            rowIsMain = funcoesUteis.analyzeIfFieldIsValid(valuesOfLine, 'row')
            if rowIsMain == "" or rowIsMain == "main":
                rowIsMain = 'not_main' if isRowCorrect is True else 'main'
            
            if nameField.lower().find('date') >= 0:
                formatDate = funcoesUteis.analyzeIfFieldIsValid(settingField, 'formatDate')
                if formatDate == 'dd/mm/aaaa':
                    formatDate = 1
                elif formatDate == 'aaaa-mm-dd':
                    formatDate = 2
                else:
                    formatDate = 1
                
                valueField = funcoesUteis.treatDateFieldInVector(data, numberField, positionsOfHeader, nameColumn, formatDate, rowIsMain)
                valueField = None if numberField == -1 and nameColumn is None else valueField

                if valueField is not None:
                    validField = True
            elif nameField.lower().find('amount') >= 0:
                valueField = funcoesUteis.treatDecimalFieldInVector(data, numberField, positionsOfHeader, nameColumn)
                valueField = 0 if numberField == -1 and nameColumn is None else valueField

                if valueField != 0:
                    validField = True
            elif nameField.lower().find('bank') >= 0:
                valueField = funcoesUteis.treatTextFieldInVector(data, numberField, positionsOfHeader, nameColumn).replace('-', ' ')
                valueField = "" if numberField == -1 and nameColumn is None else valueField

                if valueField != "" and valueField is not None:
                    validField = True
            else:
                splitField = funcoesUteis.analyzeIfFieldIsValid(settingField, 'splitField')

                valueField = funcoesUteis.treatTextFieldInVector(data, numberField, positionsOfHeader, nameColumn)
                valueField = "" if numberField == -1 and nameColumn is None else valueField

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
                valuesOfLine[nameField] = valueField  
        
        return valuesOfLine

    def getPositionFieldByName(self, settingFields, nameField):
        for positionFieldInVector, settingField in enumerate(settingFields):
            existField = funcoesUteis.analyzeIfFieldIsValid( settingField, nameField )
            if existField != "":
                return positionFieldInVector

    def updateFieldsNotMain(self, data, settingFields):
        row = funcoesUteis.analyzeIfFieldIsValid(data, 'row')

        if row == 'not_main':
            for nameField, valueField in data.items():

                positionFieldInVector = self.getPositionFieldByName(settingFields, nameField)
                if positionFieldInVector is not None:
                    fieldIsAnotherRow = funcoesUteis.analyzeIfFieldIsValid(settingFields[positionFieldInVector], 'row')
                    print(fieldIsAnotherRow)
                else:
                    fieldIsAnotherRow = ""

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

    # tem alguns sistemas que o valor do pagamento não está considerando o juros/multa/desconto, esta função faz isto
    def sumInterestFineAndDiscountInAmountPaid(self, data, isToSum=False):
        amountPaid = funcoesUteis.analyzeIfFieldIsValid(data, "amountPaid", 0.0)
        amountInterest = funcoesUteis.analyzeIfFieldIsValid(data, "amountInterest", 0.0)
        amountFine = funcoesUteis.analyzeIfFieldIsValid(data, "amountFine", 0.0)
        amountDiscount = funcoesUteis.analyzeIfFieldIsValid(data, "amountDiscount", 0.0)

        if isToSum is False:
            return amountPaid
        else:
            return amountPaid + amountInterest + amountFine - amountDiscount

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
        if len(self._validationsLineToPrint) == 0:
            return True

        countValidationsIsTrue = 0
        countValidations = 0
        for validationsLineToPrint in self._validationsLineToPrint:
            for nameField, validations in validationsLineToPrint.items():
                for validation in validations:
                    countValidations += 1

                    typeValidation = funcoesUteis.analyzeIfFieldIsValid(validation, 'typeValidation')
                    valueValidation = funcoesUteis.analyzeIfFieldIsValid(validation, 'valueValidation')

                    valueFieldData = funcoesUteis.analyzeIfFieldIsValid(data, nameField)

                    if typeValidation == "isLessThan" and valueFieldData < valueValidation:
                        countValidationsIsTrue += 1
                    elif typeValidation == "isEqual" and valueFieldData == valueValidation:
                        countValidationsIsTrue += 1
                    elif typeValidation == "isDate" and str(type(valueFieldData)).count('datetime.date') > 0:
                        countValidationsIsTrue += 1
                    elif typeValidation == "isDifferent" and valueFieldData != valueValidation:
                        countValidationsIsTrue += 1
        
        if countValidationsIsTrue == countValidations:
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
        self._validationsLineToPrint = []
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
            elif setting['fileType'] == 'csv':
                dataFile = readCsv(file)
            else:
                dataFile = []

            fields = setting['fields']
            self.analyzeSettingFieldsThatAreNecessaryData(fields)

            for data in dataFile:
                try:
                    posionsOfHeaderTemp = self.identifiesTheHeader(data, setting)                    
                    if posionsOfHeaderTemp is not None and len(posionsOfHeaderTemp) > 0:
                        if len(posionsOfHeaderTemp.items()) > 0:
                            posionsOfHeader = posionsOfHeaderTemp
                            continue

                    valuesOfLine = self.treatDataLayout(data, fields, posionsOfHeader)
                    self.updateFieldsNotMain(valuesOfLine, fields)
                    valuesOfLine = self.groupsRowData(valuesOfLine)
                    # print(valuesOfLine)
                    
                    valuesOfLine['bank'] = funcoesUteis.analyzeIfFieldIsValid(valuesOfLine, 'bank') # o banco é um campo obrigatório na ordenação do Excel. Portanto, se não existir ele vai dar erro. Por isto desta linha. 
                    
                    # colocar um campo pra verificar esta linha depois, não é toda vez que deve somar. Pois pode ser que o valor pago já vem com o juros/multa/desconto
                    valuesOfLine['amountPaid'] = self.sumInterestFineAndDiscountInAmountPaid(valuesOfLine, True)

                    # juros e desconto sai repetido no relatório do cliente, pois já vem na coluna de juros e multa, então ignoro
                    # tirar esta linha, é apenas temporária
                    accountPlan = funcoesUteis.analyzeIfFieldIsValid(valuesOfLine, 'accountPlan')
                    if accountPlan == "MULTA E JUROS DE MORA" or accountPlan == "DESCONTOS OBTIDOS":
                        continue
                    
                    isValid = self.isValidLineToPrint(valuesOfLine)
                    # isValid = True
                    if isValid is True:
                        if layoutType == 'account_paid':
                            valuesOfLine['numberLote'] = self.handleLayoutIsPartidaMultipla(valuesOfLine, valuesOfFilePayments)
                            valuesOfFilePayments.append(valuesOfLine.copy())
                        elif layoutType == 'extract_bank':
                            valuesOfFileExtracts.append(valuesOfLine.copy())

                except Exception as e:
                    print(e.with_traceback())
                    
        # soma o total pago por lote
        valuesOfFilePayments = self.sumAmountPaidPerLote(valuesOfFilePayments)

        return [valuesOfFilePayments, valuesOfFileExtracts]

    def processAll(self):
        for root, dirs, files in os.walk(self._wayOriginalToRead):
            for file in files:
                wayFile = os.path.join(root, file)

                if file.lower().endswith(('.xls', '.xlsx', '.csv')):
                    process = self.process(wayFile)
                    self._payments.append(process[0])
                    self._extracts.append(process[1])

        return [funcoesUteis.removeAnArrayFromWithinAnother(self._payments), funcoesUteis.removeAnArrayFromWithinAnother(self._extracts)]



if __name__ == "__main__":

    from dao.src.GetSettingsCompany import GetSettingsCompany

    codi_emp = 1498

    getSettingsCompany = GetSettingsCompany(codi_emp)
    settings = getSettingsCompany.getSettingsFinancy()

    readFiles = ReadGeneral(codi_emp, f"C:/integracao_contabil/{codi_emp}/arquivos_originais", settings)
    print(readFiles.processAll()[0])
