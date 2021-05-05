import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(absPath[:absPath.find('extract')])

import tools.funcoesUteis as funcoesUteis

class Pagamento(object):
    def __init__(self, dataFile, file):
        self._dataFile = dataFile
        self._file = file
        self._accountDebitOrCredit = ''

    def process(self):
        valuesOfLine = {}

        isPagamento = False

        nameProvider = ""
        historic = ""
        amountPaid = float(0)
        account = ""
        amountOriginal = float(0)
        amountDiscount = float(0)
        amountInterest = float(0)
        amountFine = float(0)
        paymentDate = None
        dueDate = None
        
        for data in self._dataFile:
            if isPagamento == False and data.find('COMPROVANTE DE PAGAMENTO') >= 0:
                isPagamento = True

            data = str(data)
            dataSplit = data.split(':')

            fieldOne = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 1))
            fieldTwo = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 2))
            fieldThree = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 3))
            
            if fieldOne.count('DO DOCUMENTO') > 0 and fieldTwo.count("DATA") > 0:
                paymentDate = funcoesUteis.retornaCampoComoData(fieldThree)

            if fieldOne == 'CONTA':
                account = funcoesUteis.treatNumberField(fieldTwo)

            if fieldOne.count('BENEFICIARIO') > 0:
                self._accountDebitOrCredit = 'DEBIT'
            elif fieldOne.count('PAGADOR') > 0:
                self._accountDebitOrCredit = 'CREDIT'
            elif fieldOne.count('SACADOR') > 0:
                self._accountDebitOrCredit = ''

            if self._accountDebitOrCredit == 'DEBIT':
                if fieldOne == 'RAZAO SOCIAL':
                    nameProvider = fieldTwo              
                if fieldOne == 'CNPJ/CPF':
                    cgceProvider = fieldTwo      

            elif self._accountDebitOrCredit == 'CREDIT':
                if fieldOne == "DATA DO PAGAMENTO":
                    paymentDate = funcoesUteis.retornaCampoComoData(fieldTwo)
                if fieldOne == "DATA DE VENCIMENTO":
                    dueDate = funcoesUteis.retornaCampoComoData(fieldTwo)
                if fieldOne == "VALOR NOMINAL":
                    amountOriginal = funcoesUteis.treatDecimalField(fieldTwo)
                if fieldOne == 'ENCARGOS':
                    amountInterest = funcoesUteis.treatDecimalField(fieldTwo)
                if fieldOne == "VALOR PAGO":
                    amountPaid = funcoesUteis.treatDecimalField(fieldTwo)
                if fieldOne == "DESCONTO":
                    amountDiscount = funcoesUteis.treatDecimalField(fieldTwo)

            if fieldOne == "VALOR PAGO":
                if paymentDate is not None and amountPaid > 0 and isPagamento is True:
                    valuesOfLine = {
                        "paymentDate": paymentDate,
                        "nameProvider": nameProvider,
                        "cgceProvider": cgceProvider,
                        "dueDate": dueDate,
                        "bank": 'AMAZONIA',
                        "account": account,
                        "amountPaid": round(amountPaid, 2),
                        "amountInterest": round(amountInterest, 2),
                        "amountDiscount": round(amountDiscount, 2),
                        "amountFine": round(amountFine, 2),
                        "amountOriginal": round(amountOriginal, 2),
                        "historic": historic,
                        "category": 'PAGAMENTO',
                        "cgcePaying": "",
                        "foundProof": True,
                        "amountPaidPerLote": round(amountPaid, 2),
                        "wayFile": self._file
                    }

                    return valuesOfLine.copy()