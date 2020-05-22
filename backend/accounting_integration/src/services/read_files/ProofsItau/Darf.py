import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import tools.funcoesUteis as funcoesUteis

class Darf(object):
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
        
        for data in self._dataFile:
            if isDarf == False and data.find('PAGAMENTO DARF') >= 0:
                isDarf = True

            data = str(data)
            dataSplit = data.split(':')

            fieldOne = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 1))
            fieldTwo = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 2))

            if fieldOne.count('CONTA DEBITADA') > 0:
                self._accountDebitOrCredit = 'DEBIT'
            elif fieldOne.count('AGENTE ARRECADOR') > 0:
                self._accountDebitOrCredit = 'CREDIT'

            if self._accountDebitOrCredit == 'DEBIT':
                if fieldOne.count('AGENCIA/CONTA') > 0:
                    account = fieldTwo.split()
                    account = funcoesUteis.analyzeIfFieldIsValidMatrix(account, 2)
                if fieldOne.count('CPF OU CNPJ') > 0:
                    nameProvider = f"DARF - {fieldTwo}"
            elif self._accountDebitOrCredit == 'CREDIT':
                if fieldOne == "DATA DO PAGAMENTO":
                    paymentDate = funcoesUteis.retornaCampoComoData(fieldTwo)
                if fieldOne == "VALOR PRINCIPAL":
                    amountOriginal = funcoesUteis.treatDecimalField(fieldTwo)
                if fieldOne == "DESCONTO":
                    amountDiscount = funcoesUteis.treatDecimalField(fieldTwo)
                if fieldOne == "VALOR DOS JUROS/ENCARGOS":
                    amountInterest = funcoesUteis.treatDecimalField(fieldTwo)
                if fieldOne == "VALOR DA MULTA":
                    amountFine = funcoesUteis.treatDecimalField(fieldTwo)
                if fieldOne == "VALOR TOTA":
                    amountPaid = funcoesUteis.treatDecimalField(fieldTwo)       

            if fieldOne.count('AGENCIA/CONTA') > 0:
                if paymentDate is not None and amountPaid > 0 and isDarf is True:
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
                        "category": 'DARF',
                        "cgcePaying": "",
                        "foundProof": True,
                        "amountPaidPerLote": round(amountPaid, 2)
                    }

                    return valuesOfLine.copy()

            