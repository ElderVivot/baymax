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
        self._validationsLineToPrint = [] # vai salvar os critérios pra ver se uma linha é válida pra gerar o lançamento ou não
        self._sumInterestFineAndDiscount = False
        self._informationIsOnOneLineBelowTheMain = False
        self._fieldsThatMultiplePerLessOne = {}

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

    def identifiesIfTheRowCorrect(self, dataIsNotLineMain, data):
        if len(dataIsNotLineMain) == 0:
            return None

        countHeaderEquals = 0

        for dataIsNotLineMainValidation in dataIsNotLineMain:
            positionInFile = funcoesUteis.analyzeIfFieldIsValid(dataIsNotLineMainValidation, 'positionInFile', -1)
            positionInFileEnd = funcoesUteis.analyzeIfFieldIsValid(dataIsNotLineMainValidation, 'positionInFileEnd', -1)
            typeValidation = funcoesUteis.analyzeIfFieldIsValid(dataIsNotLineMainValidation, 'typeValidation')
            valueValidation = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValid(dataIsNotLineMainValidation, 'valueValidation'))
            valueFieldData = funcoesUteis.treatTextFieldInVector(data, positionInFile, positionInFileEnd=positionInFileEnd)
            
            if typeValidation == "isDate":
                valueFieldDate = funcoesUteis.retornaCampoComoData(valueFieldData) if len(valueFieldData) <= 10 else None # este campo é pra caso tenha algum valor que seja data + horário ele não cai na verificação do isDate
                if valueFieldDate is not None:
                    countHeaderEquals += 1
            elif typeValidation == "isEqual" and valueValidation == valueFieldData:
                countHeaderEquals += 1
            elif typeValidation == "contains" and valueFieldData.find(valueValidation) >= 0:
                countHeaderEquals += 1
        
        if countHeaderEquals == len(dataIsNotLineMain):
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

            if nameField == "amountPaid":
                self._sumInterestFineAndDiscount = funcoesUteis.analyzeIfFieldIsValid(settingField, 'sumInterestFineAndDiscount', False)

            self._informationIsOnOneLineBelowTheMain = funcoesUteis.analyzeIfFieldIsValid(settingField, 'informationIsOnOneLineBelowTheMain', False)

            self._fieldsThatMultiplePerLessOne[nameField] = funcoesUteis.analyzeIfFieldIsValid(settingField, 'multiplePerLessOne', False)

    def treatDataLayout(self, data, settingFields, positionsOfHeader, readOnlyRowIsNotMain=False):
        # o readOnlyRowIsNotMain serve pra ler as linhas que estão uma abaixo da principal, pra poder agrupar com a linha anterior
        valuesOfLine = {}
        positionsOfHeaderCorrect = positionsOfHeader

        for settingField in settingFields:
            nameField = funcoesUteis.analyzeIfFieldIsValid(settingField, 'nameField')

            positionInFile = funcoesUteis.analyzeIfFieldIsValid(settingField, 'positionInFile', -1)
            positionInFileEnd = funcoesUteis.analyzeIfFieldIsValid(settingField, 'positionInFileEnd', -1)

            nameColumn = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValid(settingField, 'nameColumn'))
            nameColumn = None if nameColumn == "" else nameColumn

            valueDefault = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValid(settingField, 'valueDefault'))

            validField = False

            # esta row é apenas pra identificar se a informação está na linha principal ou não, caso não esteja, vai guardar seu valor
            # na self._fieldsRowNotMain pra serem utilizados na linha principal depois         
            dataIsNotLineMain = funcoesUteis.analyzeIfFieldIsValid(settingField, 'dataIsNotLineMain')
            isRowCorrect = self.identifiesIfTheRowCorrect(dataIsNotLineMain, data)
            
            rowIsMain = funcoesUteis.analyzeIfFieldIsValid(valuesOfLine, 'row')
            if rowIsMain == "" or rowIsMain == "main":                
                if isRowCorrect is True:
                    rowIsMain = 'not_main'
                    positionsOfHeaderCorrect = {}
                else:
                    rowIsMain = 'main'
            
            # quando não é uma linha main ele apenas dá seguinte processando ela se de fato for uma linha not_main já passado pela validação do isRowCorrect,
            # ou seja, só retorna o dado se de fato a validação do campo é válida
            if dataIsNotLineMain != "" and isRowCorrect is not True:
                continue
            
            # caso não seja uma linha prinpial e o argumento readOnlyRowIsNotMain seja True então ignora pra parar o processamento
            if readOnlyRowIsNotMain is True and rowIsMain == 'main':
                continue

            if nameField.lower().find('date') >= 0:
                formatDate = funcoesUteis.analyzeIfFieldIsValid(settingField, 'formatDate')
                if formatDate == 'dd/mm/aaaa':
                    formatDate = 1
                elif formatDate == 'aaaa-mm-dd':
                    formatDate = 2
                else:
                    formatDate = 1
                
                valueField = funcoesUteis.treatDateFieldInVector(data, positionInFile, positionsOfHeaderCorrect, nameColumn, formatDate, rowIsMain, positionInFileEnd=positionInFileEnd)
                valueField = None if positionInFile == -1 and nameColumn is None else valueField

                if valueField is not None:
                    validField = True
            elif nameField.lower().find('amount') >= 0:
                valueField = funcoesUteis.treatDecimalFieldInVector(data, positionInFile, positionsOfHeaderCorrect, nameColumn, positionInFileEnd=positionInFileEnd)
                valueField = 0 if positionInFile == -1 and nameColumn is None else valueField

                if valueField != 0:
                    validField = True
            elif nameField.lower().find('bank') >= 0:
                valueField = funcoesUteis.treatTextFieldInVector(data, positionInFile, positionsOfHeaderCorrect, nameColumn, positionInFileEnd=positionInFileEnd).replace('-', ' ')
                valueField = funcoesUteis.minimalizeSpaces(valueField)
                valueField = "" if positionInFile == -1 and nameColumn is None else valueField
                
                if valueField != "" and valueField is not None:
                    validField = True
            elif nameField.lower() == 'document':
                valueField = funcoesUteis.treatTextFieldInVector(data, positionInFile, positionsOfHeaderCorrect, nameColumn, positionInFileEnd=positionInFileEnd)
                hasHyphen = valueField.find('-')
                hasBackslash = valueField.find('/')

                if hasHyphen >= 0 and hasBackslash == -1:
                    valueField = valueField.split('-')[0]
                elif hasHyphen == -1 and hasBackslash >= 0:
                    valueField = valueField.split('/')[0]
                else:
                    if hasHyphen < hasBackslash:
                        valueField = valueField.split('-')[0]
                    else:
                        valueField = valueField.split('/')[0]

                valueField = funcoesUteis.minimalizeSpaces(valueField)
                valueField = "" if positionInFile == -1 and nameColumn is None else valueField

                if valueField == "":
                    valueField = None
                
                if valueField != "" or valueField is not None:
                    validField = True
            else:
                splitField = funcoesUteis.analyzeIfFieldIsValid(settingField, 'splitField')

                valueField = funcoesUteis.treatTextFieldInVector(data, positionInFile, positionsOfHeaderCorrect, nameColumn, positionInFileEnd=positionInFileEnd)
                valueField = "" if positionInFile == -1 and nameColumn is None else valueField

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

    def getPositionFieldByNameField(self, settingFields, nameFieldSearch):
        for positionFieldInVector, settingField in enumerate(settingFields):
            nameField = funcoesUteis.analyzeIfFieldIsValid( settingField, 'nameField' )
            if nameField == nameFieldSearch:
                return positionFieldInVector

    def updateFieldsNotMain(self, data, settingFields):
        # :data é os dados com informações dos campos daquela linha
        # :settingFields é o vetor de configuração de cada campo que fica no 'fields'
        row = funcoesUteis.analyzeIfFieldIsValid(data, 'row')

        if row == 'not_main':
            for nameField, valueField in data.items():

                # pega a posição do campo do vetor do fields da tabela IntegrattionLayouts
                positionFieldInVector = self.getPositionFieldByNameField(settingFields, nameField)
                if positionFieldInVector is not None:
                    fieldIsAnotherRow = funcoesUteis.analyzeIfFieldIsValid(settingFields[positionFieldInVector], 'dataIsNotLineMain', None)
                else:
                    fieldIsAnotherRow = None

                # faz validação dos campos pra ver se devem ser atualizados as informações ou não
                if fieldIsAnotherRow is not None:
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
    def sumInterestFineAndDiscountInAmountPaid(self, data):
        amountPaid = funcoesUteis.analyzeIfFieldIsValid(data, "amountPaid", 0.0)
        amountInterest = funcoesUteis.analyzeIfFieldIsValid(data, "amountInterest", 0.0)
        amountFine = funcoesUteis.analyzeIfFieldIsValid(data, "amountFine", 0.0)
        amountDiscount = funcoesUteis.analyzeIfFieldIsValid(data, "amountDiscount", 0.0)

        if self._sumInterestFineAndDiscount is False:
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

    # tem alguns sistemas que trás o valor negativo como sendo o pago, tem que multiplicar por menos 1 pra ficar certo
    def multiplePerLessOneWhenNecessary(self, valuesOfLine):
        for nameField, valueField in valuesOfLine.items():
            if funcoesUteis.analyzeIfFieldIsValid(self._fieldsThatMultiplePerLessOne, nameField, False) is True:
                valuesOfLine[nameField] = valueField * (-1)
        
        return valuesOfLine

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
        self._sumInterestFineAndDiscount = False
        self._fieldsThatMultiplePerLessOne = {}
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
            # esta linha é útil pois vários campos preciso guardar as configurações dele pra verificações futuras
            self.analyzeSettingFieldsThatAreNecessaryData(fields)

            for key, data in enumerate(dataFile):
                try:
                    posionsOfHeaderTemp = self.identifiesTheHeader(data, setting)                    
                    if posionsOfHeaderTemp is not None and len(posionsOfHeaderTemp) > 0:
                        if len(posionsOfHeaderTemp.items()) > 0:
                            posionsOfHeader = posionsOfHeaderTemp
                            continue

                    # quando as informações complementares estão uma linha abaixo da principal então lê ela primeiro e atualiza os campos notMain
                    if self._informationIsOnOneLineBelowTheMain is True:
                        nextData = funcoesUteis.analyzeIfFieldIsValidMatrix(dataFile, key+1, positionOriginal=True)
                        valuesOfLine = self.treatDataLayout(nextData, fields, posionsOfHeader, readOnlyRowIsNotMain=True)
                        self.updateFieldsNotMain(valuesOfLine, fields)

                    valuesOfLine = self.treatDataLayout(data, fields, posionsOfHeader)
                    self.updateFieldsNotMain(valuesOfLine, fields)
                    valuesOfLine = self.groupsRowData(valuesOfLine)
                    
                    valuesOfLine['bank'] = funcoesUteis.analyzeIfFieldIsValid(valuesOfLine, 'bank') # o banco é um campo obrigatório na ordenação do Excel. Portanto, se não existir ele vai dar erro. Por isto desta linha. 
                    
                    # ele verifica se é necessário somar juros/multa e subtrair o desconto no valor pago
                    valuesOfLine['amountPaid'] = self.sumInterestFineAndDiscountInAmountPaid(valuesOfLine)

                    isValid = self.isValidLineToPrint(valuesOfLine)                    
                    if isValid is True:
                        valuesOfLine = self.multiplePerLessOneWhenNecessary(valuesOfLine)
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

    codi_emp = 425

    getSettingsCompany = GetSettingsCompany(codi_emp)
    settings = getSettingsCompany.getSettingsFinancy()

    readFiles = ReadGeneral(codi_emp, f"C:/integracao_contabil/{codi_emp}/arquivos_originais", settings)
    print(readFiles.processAll()[0])

