import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import json
from tools.leArquivos import leXls_Xlsx, leTxt, readJson
import tools.funcoesUteis as funcoesUteis


class PaymentsGeneral(object):

    def __init__(self, codiEmp, wayOriginalToRead, settings):
        self._codiEmp = codiEmp
        self._wayOriginalToRead = wayOriginalToRead
        self._settings = settings
        self._payments = []

    # def isPayment(self, file):
    #     dataFile = leXls_Xlsx(file)

    #     for data in dataFile:
    #         textComparateOne = funcoesUteis.treatTextFieldInVector(data, 2)

    #         textCompara = funcoesUteis.treatTextFieldInVector(data, 8)

    #         if textHistoric == "HISTORICO" and ( textUser == "USU.LANC." or textUser == "USU. LANC." ):
    #             return True

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

    def treatDataLayout(self, data, settingFields, positionsOfHeader):
        valuesOfLine = {}

        for key, settingField in settingFields.items():
            numberField = funcoesUteis.analyzeIfFieldIsValid(settingField, 'numberField')
            nameField = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValid(settingField, 'nameField'))
            
            if key.find('date') >= 0:
                formatDate = funcoesUteis.analyzeIfFieldIsValid(settingField, 'formatDate')
                if formatDate == 'dd/mm/aaaa':
                    formatDate = 1
                elif formatDate == 'aaaa-mm-dd':
                    formatDate = 2
                else:
                    formatDate = 1
                
                valuesOfLine[key] = funcoesUteis.treatDateFieldInVector(data, numberField, positionsOfHeader, nameField, formatDate)
            elif key.find('amount') >= 0:
                valuesOfLine[key] = funcoesUteis.treatDecimalFieldInVector(data, numberField, positionsOfHeader, nameField)
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

                valuesOfLine[key] = valueField

        return valuesOfLine

    def process(self, file):
        settingsLayouts = funcoesUteis.analyzeIfFieldIsValid( self._settings, 'settingsLayouts')

        if len(settingsLayouts) == 0:
            return None

        valuesOfLine = {}
        valuesOfFile = []
        posionsOfHeader = {}

        for setting in settingsLayouts:
            
            if setting['layoutType'] != "Financy":
                return None
            
            if setting['fileType'] == 'Excel':
                dataFile = leXls_Xlsx(file)
            else:
                dataFile = []

            fields = setting['fields']

            for key, data in enumerate(dataFile):

                try:
                    posionsOfHeaderTemp = self.identifiesTheHeader(data, setting)
                    if len(posionsOfHeaderTemp.items()) > 0:
                        posionsOfHeader = posionsOfHeaderTemp
                        continue

                    valuesOfLine = self.treatDataLayout(data, fields, posionsOfHeader)
                    
                    paymentDate = funcoesUteis.retornaCampoComoData(funcoesUteis.analyzeIfFieldIsValid(valuesOfLine, 'paymentDate', None))
                    amountPaid = funcoesUteis.analyzeIfFieldIsValid(valuesOfLine, 'amountPaid', 0)
                    valuesOfLine['bank'] = funcoesUteis.analyzeIfFieldIsValid(valuesOfLine, 'bank') # o banco é um campo obrigatório na ordenação do Excel. Portanto, se não existir ele vai dar erro. Por isto desta linha. 
                    
                    if paymentDate is not None and amountPaid > 0:
                        valuesOfFile.append(valuesOfLine.copy())

                except Exception as e:
                    pass

        return valuesOfFile

    def processAll(self):
        for root, dirs, files in os.walk(self._wayOriginalToRead):
            for file in files:
                wayFile = os.path.join(root, file)

                if file.lower().endswith(('.xls', '.xlsx')):
                    self._payments.append(self.process(wayFile))

        return funcoesUteis.removeAnArrayFromWithinAnother(self._payments)

if __name__ == "__main__":

    payments = PaymentsGeneral(1342, "C:/integracao_contabil/1342/arquivos_originais", "")
    print(payments.processAll())

