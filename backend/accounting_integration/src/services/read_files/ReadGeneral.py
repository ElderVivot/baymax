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
        self._sumInterestFineAndDiscount = False # alguns valores amountPaid não vem com o juros/multa somados, este é pra definir isto
        self._informationIsOnOneLineBelowTheMain = False # são para informações que estão uma linha abaixo da main
        self._fieldsThatMultiplePerLessOne = {} # alguns campos vem com valor negativo, tem que multiplicar por menos 1

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

        countValidationsOK = 0
        countValidationsConfigured = 0

        for key, dataIsNotLineMainValidation in enumerate(dataIsNotLineMain):
            positionInFile = funcoesUteis.analyzeIfFieldIsValid(dataIsNotLineMainValidation, 'positionInFile', -1)
            positionInFileEnd = funcoesUteis.analyzeIfFieldIsValid(dataIsNotLineMainValidation, 'positionInFileEnd', -1)
            typeValidation = funcoesUteis.analyzeIfFieldIsValid(dataIsNotLineMainValidation, 'typeValidation')
            valueValidation = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValid(dataIsNotLineMainValidation, 'valueValidation'))
            nextValidationOrAnd = funcoesUteis.analyzeIfFieldIsValid(dataIsNotLineMainValidation, 'nextValidationOrAnd', 'and')
            valueFieldData = funcoesUteis.treatTextFieldInVector(data, positionInFile, positionInFileEnd=positionInFileEnd)

            if nextValidationOrAnd == 'and' or key == len(dataIsNotLineMain)-1:
                countValidationsConfigured += 1
            
            if typeValidation == "isDate":
                valueFieldDate = funcoesUteis.retornaCampoComoData(valueFieldData) if len(valueFieldData) <= 10 else None # este campo é pra caso tenha algum valor que seja data + horário ele não cai na verificação do isDate
                if valueFieldDate is not None:
                    countValidationsOK += 1
            elif typeValidation == "isEqual" and valueValidation == valueFieldData:
                countValidationsOK += 1
            elif typeValidation == "contains" and valueFieldData.find(valueValidation) >= 0:
                countValidationsOK += 1
            elif typeValidation == "notContains" and valueFieldData.find(valueValidation) == -1:
                countValidationsOK += 1
        
        if countValidationsOK == countValidationsConfigured:
            return True

    # avalia quais configurações são importantes pro processamento de outros campos, tais como _groupingFields, _validationsLineToPrint, etc
    # além disso, ele reagrupa os fields pra trazer primeiro o que tem o atributo dataIsNotLineMain, pra depois trazer os  que não tem
    # isto é necessário afim de que um campo numa linha not_main ele só seja preenchido se de fato ele tiver naquela linha
    def analyzeSettingFields(self, settingFields):
        fieldsHasDataIsNotLineMain = []
        fieldsDontHasDataIsNotLineMain = []

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

            if self._informationIsOnOneLineBelowTheMain is False:
                self._informationIsOnOneLineBelowTheMain = funcoesUteis.analyzeIfFieldIsValid(settingField, 'informationIsOnOneLineBelowTheMain', False)

            self._fieldsThatMultiplePerLessOne[nameField] = funcoesUteis.analyzeIfFieldIsValid(settingField, 'multiplePerLessOne', False)

            dataIsNotLineMain = funcoesUteis.analyzeIfFieldIsValid(settingField, 'dataIsNotLineMain', '')
            if dataIsNotLineMain != "":
                fieldsHasDataIsNotLineMain.append(settingField)
            else:
                fieldsDontHasDataIsNotLineMain.append(settingField)
        
        return funcoesUteis.removeAnArrayFromWithinAnother([fieldsHasDataIsNotLineMain, fieldsDontHasDataIsNotLineMain])

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
            
            # esta row é apenas pra identificar se a informação está na linha principal ou não, caso não esteja, vai guardar seu valor
            # na self._fieldsRowNotMain pra serem utilizados na linha principal depois         
            dataIsNotLineMain = funcoesUteis.analyzeIfFieldIsValid(settingField, 'dataIsNotLineMain', '')
            isRowCorrect = self.identifiesIfTheRowCorrect(dataIsNotLineMain, data)
            
            rowIsMain = funcoesUteis.analyzeIfFieldIsValid(valuesOfLine, 'row')
            if rowIsMain == "" or rowIsMain == "main":                
                if isRowCorrect is True:
                    rowIsMain = 'not_main'
                    positionsOfHeaderCorrect = {}
                else:
                    rowIsMain = 'main'
            
            # se não for a linha correta mas o campo seja referente a uma linha notMain então ignora, pois este campo não é válido nesta linha
            if isRowCorrect is None and dataIsNotLineMain != "":
                continue

            # se a linha for "not_main" mas o isRowCorrect não retornar resultado, então quer dizer que aquele campo não é daquela linha not_main. Pode ser de outra.
            if rowIsMain == "not_main" and isRowCorrect is None:
                continue
            
            # se o isRowCorrect não for válido e estou exigindo que seja eita apenas uma linha not_main então ignora, visto que isRowCorrect é apenas pra linhas not_main
            if readOnlyRowIsNotMain is True and isRowCorrect is None:
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

            elif nameField.lower().find('amount') >= 0:
                valueField = funcoesUteis.treatDecimalFieldInVector(data, positionInFile, positionsOfHeaderCorrect, nameColumn, positionInFileEnd=positionInFileEnd)
                valueField = 0 if positionInFile == -1 and nameColumn is None else valueField

            else:
                splitField = funcoesUteis.analyzeIfFieldIsValid(settingField, 'splitField')
                positionFieldInTheSplit = funcoesUteis.analyzeIfFieldIsValid(settingField, 'positionFieldInTheSplit', 0)
                positionFieldInTheSplitEnd = funcoesUteis.analyzeIfFieldIsValid(settingField, 'positionFieldInTheSplitEnd', 0) # o zero determina que não tem fim, é daquele campo pra frente

                valueField = funcoesUteis.treatTextFieldInVector(data, positionInFile, positionsOfHeaderCorrect, nameColumn, positionInFileEnd=positionInFileEnd)
                valueField = "" if positionInFile == -1 and nameColumn is None else valueField

                if splitField != "":
                    valueField = valueField.split(splitField)
                    if len(valueField) >= positionFieldInTheSplit and positionFieldInTheSplit != 0:
                        if positionFieldInTheSplitEnd != 0:
                            valueField = ''.join(valueField[positionFieldInTheSplit-1:positionFieldInTheSplitEnd])
                        else:
                            valueField = ''.join(valueField[positionFieldInTheSplit-1:])
                    else:
                        valueField = ""
                    valueField = funcoesUteis.minimalizeSpaces(valueField)
                
                if nameField == "account":
                    valueField = funcoesUteis.minimalizeSpaces(valueField.replace('-', ''))
                    valueField = funcoesUteis.treatNumberField(valueField, True)
                    valueField = "" if valueField == 0 else str(valueField)
                
                if nameField == "bank":
                    valueField = funcoesUteis.minimalizeSpaces(valueField.replace('-', ''))
                    # valueField = funcoesUteis.returnBankForName(valueField)
                    # valueField = funcoesUteis.returnBankForNumber(valueField)
            
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
                    dataIsNotLineMain = funcoesUteis.analyzeIfFieldIsValid(settingFields[positionFieldInVector], 'dataIsNotLineMain', None)
                else:
                    dataIsNotLineMain = None

                # faz validação dos campos pra ver se devem ser atualizados as informações ou não
                if dataIsNotLineMain is not None:
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

    def correlationBankAndAccountBetweenSettingsAndClient(self, valuesOfLine, bankAndAccountCorrelation):
        # :valuesOfLine é o banco que vem lá do financeiro do cliente já passado pelo treatDataLayout
        # :bankAndAccountCorrelation recebe as configurações do de-para dos bancos

        bankFinancy = funcoesUteis.analyzeIfFieldIsValid(valuesOfLine, 'bank')
        accountFinancy = funcoesUteis.analyzeIfFieldIsValid(valuesOfLine, 'account')

        if bankAndAccountCorrelation is not None:
            for correlation in bankAndAccountCorrelation:
                correlationBankFile = funcoesUteis.treatTextFieldInDictionary(correlation, 'bankFile').replace('-', '')
                correlationAccountFile = str(funcoesUteis.treatNumberFieldInDictionary(correlation, 'accountFile', isInt=True)).replace('-', '')
                correlationAccountFile = "" if correlationAccountFile == "0" else correlationAccountFile
                
                correlationBankNew = funcoesUteis.treatTextFieldInDictionary(correlation, 'bankNew').replace('-', '')
                correlationAccountNew = str(funcoesUteis.treatNumberFieldInDictionary(correlation, 'accountNew', isInt=True)).replace('-', '')
                correlationAccountNew = "" if correlationAccountNew == "0" else correlationAccountNew

                if bankFinancy == correlationBankFile and accountFinancy == correlationAccountFile:
                    valuesOfLine['bank'] = correlationBankNew
                    valuesOfLine['account'] = correlationAccountNew
                    break
                else:
                    valuesOfLine['bank'] = bankFinancy
                    valuesOfLine['account'] = accountFinancy
        else:
            valuesOfLine['bank'] = funcoesUteis.returnBankForNumber(funcoesUteis.returnBankForName(bankFinancy))
            valuesOfLine['account'] = accountFinancy
        
        return valuesOfLine

    def bankAndAccountInTheCorrelation(self, bank, account, bankAndAccountCorrelation):
        # :valuesOfLine é o banco que vem lá do financeiro do cliente já passado pelo treatDataLayout
        # :bankAndAccountCorrelation recebe as configurações do de-para dos bancos
        if bankAndAccountCorrelation is None:
            return True

        for correlation in bankAndAccountCorrelation:
            correlationBankNew = funcoesUteis.treatTextFieldInDictionary(correlation, 'bankNew').replace('-', '')
            correlationAccountNew = str(funcoesUteis.treatNumberFieldInDictionary(correlation, 'accountNew', isInt=True)).replace('-', '')
            correlationAccountNew = "" if correlationAccountNew == "0" else correlationAccountNew

            if bank == correlationBankNew and account == correlationAccountNew:
                return True

    def isValidDataThisCompanie(self, valuesOfLine, validateIfDataIsThisCompanie, bankAndAccountCorrelation):
        """
        :param valuesOfLine: valores normais da linha onde a verificação será será feita
        :parm validateIfDataIsThisCompanie: configurações do IntegrattionCompanies onde tem as verificações pra ver é uma linha válida ou não
        """
        if validateIfDataIsThisCompanie is None:
            return True
        
        countValidationsOK = 0
        countValidationsConfigured = 0

        for key, validate in enumerate(validateIfDataIsThisCompanie):
            typeValidation = funcoesUteis.analyzeIfFieldIsValid(validate, 'typeValidation')
            nextValidationOrAnd = funcoesUteis.analyzeIfFieldIsValid(validateIfDataIsThisCompanie, 'nextValidationOrAnd', 'and')

            if nextValidationOrAnd == 'and' or key == len(validateIfDataIsThisCompanie)-1:
                countValidationsConfigured += 1

            if typeValidation == "banksInTheCorrelation":
                bank = funcoesUteis.analyzeIfFieldIsValid(valuesOfLine, 'bank')
                account = funcoesUteis.analyzeIfFieldIsValid(valuesOfLine, 'account')
                bankAndAccountInTheCorrelation = self.bankAndAccountInTheCorrelation(bank, account, bankAndAccountCorrelation)
                if bankAndAccountInTheCorrelation is True:
                    countValidationsOK += 1

        if countValidationsOK == countValidationsConfigured:
            return True
    
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
            elif setting['fileType'] == 'txt':
                dataFile = leTxt(file)
            else:
                dataFile = []

            fields = setting['fields']
            fields = self.analyzeSettingFields(fields)

            bankAndAccountCorrelation = funcoesUteis.analyzeIfFieldIsValid(setting, 'bankAndAccountCorrelation')
            validateIfDataIsThisCompanie = funcoesUteis.analyzeIfFieldIsValid(setting, 'validateIfDataIsThisCompanie')

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
                    
                    valuesOfLine = self.correlationBankAndAccountBetweenSettingsAndClient(valuesOfLine, bankAndAccountCorrelation)
                    # ele verifica se é necessário somar juros/multa e subtrair o desconto no valor pago
                    valuesOfLine['amountPaid'] = self.sumInterestFineAndDiscountInAmountPaid(valuesOfLine)

                    isValid = self.isValidLineToPrint(valuesOfLine)
                    isValidDataThisCompanie = self.isValidDataThisCompanie(valuesOfLine, validateIfDataIsThisCompanie, bankAndAccountCorrelation)              
                    if isValid is True and isValidDataThisCompanie is True:
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

                if file.lower().endswith(('.xls', '.xlsx', '.csv', '.html')):
                    process = self.process(wayFile)
                    self._payments.append(process[0])
                    self._extracts.append(process[1])

        return [funcoesUteis.removeAnArrayFromWithinAnother(self._payments), funcoesUteis.removeAnArrayFromWithinAnother(self._extracts)]



if __name__ == "__main__":

    from dao.src.GetSettingsCompany import GetSettingsCompany

    codi_emp = 1117

    getSettingsCompany = GetSettingsCompany(codi_emp)
    settings = getSettingsCompany.getSettingsFinancy()

    readFiles = ReadGeneral(codi_emp, f"C:/integracao_contabil/{codi_emp}/arquivos_originais", settings)
    print(readFiles.processAll()[0])

