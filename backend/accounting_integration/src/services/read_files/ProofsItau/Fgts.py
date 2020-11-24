import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import tools.funcoesUteis as funcoesUteis

class Fgts(object):
    def __init__(self, dataFile):
        self._dataFile = dataFile
        self._accountDebitOrCredit = ''

    def process(self):
        valuesOfLine = {}

        isFgts = False

        nameProvider = ""
        historic = ""
        amountPaid = float(0)
        account = ""
        amountOriginal = float(0)
        amountDiscount = float(0)
        amountInterest = float(0)
        amountFine = float(0)
        paymentDate = None
        
        for data in self._dataFile:
            if isFgts == False and data.find('RECOLHIMENTO') >= 0 and data.find('FGTS') >= 0:
                isFgts = True

            data = str(data)
            dataSplit = data.split(':')

            fieldOne = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 1))
            fieldTwo = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 2))

            if fieldOne.count('AGENCIA') > 0 and fieldOne.count('CONTA') > 0:
                account = fieldTwo.split('/')
                account = funcoesUteis.analyzeIfFieldIsValidMatrix(account, 2)
                account = str(funcoesUteis.treatNumberField(account))            
            if fieldOne == "PAGAMENTO EFETUADO EM":
                paymentDate = funcoesUteis.retornaCampoComoData(fieldTwo)
            if fieldOne == "VALOR RECOLHIDO":
                amountPaid = funcoesUteis.treatDecimalField(fieldTwo)
            if fieldOne.count('DESCRICAO DO PAGAMENTO') > 0:
                nameProvider = f"RECOLHIMENTO FGTS - {fieldTwo}"    

            if paymentDate is not None and amountPaid > 0 and isFgts is True:
                valuesOfLine = {
                    "paymentDate": paymentDate,
                    "nameProvider": nameProvider,
                    "cgceProvider": "",
                    "dueDate": None,
                    "bank": 'ITAU',
                    "account": account,
                    "amountPaid": round(amountPaid, 2),
                    "amountInterest": round(amountInterest, 2),
                    "amountDiscount": round(amountDiscount, 2),
                    "amountFine": round(amountFine, 2),
                    "amountOriginal": round(amountOriginal, 2),
                    "historic": historic,
                    "category": 'FGTS - RECOLHEIMENTO',
                    "cgcePaying": "",
                    "foundProof": True,
                    "amountPaidPerLote": round(amountPaid, 2)
                }

                return valuesOfLine.copy()

            