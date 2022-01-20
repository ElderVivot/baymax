import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(absPath[:absPath.find('extract')])

import tools.funcoesUteis as funcoesUteis

class Transferencia(object):
    def __init__(self, dataFile, file):
        self._dataFile = dataFile
        self._file = file
        self._accountDebitOrCredit = ''

    def process(self):
        valuesOfLine = {}

        isTransferencia = False

        nameProvider = ""
        cgceProvider = ''
        historic = ""
        amountPaid = float(0)
        account = ""
        amountOriginal = float(0)
        amountDiscount = float(0)
        amountInterest = float(0)
        amountFine = float(0)
        paymentDate = None
        
        for data in self._dataFile:
            if isTransferencia == False and data.find('COMPROVANTE DE TRANSF') >= 0:
                isTransferencia = True

            data = str(data)
            dataSplit = data.split(':')

            fieldOne = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 1))
            fieldTwo = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 2))
            fieldThree = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 3))

            if fieldOne.count('DO DOCUMENTO') > 0:
                self._accountDebitOrCredit = 'DEBIT'
            elif fieldOne.count('FAVORECIDO') > 0:
                self._accountDebitOrCredit = 'CREDIT'
            
            if fieldTwo.count("DATA DA TRANSF") > 0:
                paymentDate = funcoesUteis.retornaCampoComoData(fieldThree)

            if self._accountDebitOrCredit == 'DEBIT':
                if fieldOne == 'CONTA':
                    account = str(funcoesUteis.treatNumberField(fieldTwo, isInt=True))

            if fieldOne == 'NOME':
                nameProvider = fieldTwo  
            if fieldOne == 'CPF':
                cgceProvider = fieldTwo            
            if fieldOne == 'CNPJ':
                cgceProvider = fieldTwo
            if fieldOne == "VALOR":
                amountPaid = funcoesUteis.treatDecimalField(fieldTwo)
            if fieldOne.count("DATA DA TRANSF") > 0:
                paymentDate = funcoesUteis.retornaCampoComoData(fieldTwo)

            if fieldOne == "DESCRICAO":
                if paymentDate is not None and amountPaid > 0 and isTransferencia is True:
                    valuesOfLine = {
                        "paymentDate": paymentDate,
                        "nameProvider": nameProvider,
                        "cgceProvider": cgceProvider,
                        "dueDate": None,
                        "bank": 'AMAZONIA',
                        "account": account,
                        "amountPaid": round(amountPaid, 2),
                        "amountInterest": round(amountInterest, 2),
                        "amountDiscount": round(amountDiscount, 2),
                        "amountFine": round(amountFine, 2),
                        "amountOriginal": round(amountOriginal, 2),
                        "historic": historic,
                        "category": 'TRANSFERENCIA',
                        "cgcePaying": "",
                        "foundProof": True,
                        "amountPaidPerLote": round(amountPaid, 2),
                        "wayFile": self._file
                    }

                    return valuesOfLine.copy()