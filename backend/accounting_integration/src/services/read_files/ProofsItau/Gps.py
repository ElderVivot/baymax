import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import tools.funcoesUteis as funcoesUteis

class Gps(object):
    def __init__(self, dataFile):
        self._dataFile = dataFile
        self._accountDebitOrCredit = ''

    def process(self):
        valuesOfLine = {}

        isDarf = False

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
            if isDarf == False and data.find('PAGAMENTO DE GPS') >= 0:
                isDarf = True

            data = str(data)
            dataSplit = data.split(':')

            fieldOne = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 1))
            fieldTwo = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 2))

            if fieldOne.count('CONTA DEBITADA') > 0:
                self._accountDebitOrCredit = 'DEBIT'
            elif fieldOne.count('AGENTE ARRECADADOR') > 0:
                self._accountDebitOrCredit = 'CREDIT'

            if self._accountDebitOrCredit == 'DEBIT':
                if fieldOne.count('AGENCIA') > 0:
                    account = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 3))
                    account = funcoesUteis.treatNumberField(account)
                    # account = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(account.split('-'), 1))
                    # if account.find(' ') > 0:
                    #     account = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(account.split(' '), 1))               
            elif self._accountDebitOrCredit == 'CREDIT':
                if fieldOne == "DATA DO PAGAMENTO":
                    paymentDate = funcoesUteis.retornaCampoComoData(fieldTwo)
                if fieldOne.count("MON/JUR/MUL") > 0:
                    amountInterest = funcoesUteis.treatDecimalField(fieldTwo)
                if fieldOne == "VALOR TOTAL":
                    amountPaid = funcoesUteis.treatDecimalField(fieldTwo)
                if fieldOne == "CODIGO DE PAGAMENTO":
                    nameProvider = f"GPS - {fieldTwo}"
                if fieldOne.count('IDENTIFICADOR') > 0:
                    cgceProvider = fieldTwo

            if fieldOne == "AGENCIA":
                if paymentDate is not None and amountPaid > 0 and isDarf is True:
                    valuesOfLine = {
                        "paymentDate": paymentDate,
                        "nameProvider": nameProvider,
                        "cgceProvider": cgceProvider,
                        "dueDate": None,
                        "bank": 'ITAU',
                        "account": account,
                        "amountPaid": round(amountPaid, 2),
                        "amountInterest": round(amountInterest, 2),
                        "amountDiscount": round(amountDiscount, 2),
                        "amountFine": round(amountFine, 2),
                        "amountOriginal": round(amountOriginal, 2),
                        "historic": historic,
                        "category": 'DARF',
                        "cgcePaying": "",
                        "foundProof": True,
                        "amountPaidPerLote": round(amountPaid, 2)
                    }

                    return valuesOfLine.copy()

            