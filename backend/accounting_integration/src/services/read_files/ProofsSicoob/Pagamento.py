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
        valuesOfFile = []
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
        countQtdDataNecessaryToProofIsValid = 0
        
        for data in self._dataFile:
            # print(data)
            if data.find('SICOOB - SISTEMA DE COOPERATIVAS') >= 0:
                countQtdDataNecessaryToProofIsValid = 0
                countQtdDataNecessaryToProofIsValid += 1

            if data.find('PAGAMENTO DE TITULO') >= 0:
                countQtdDataNecessaryToProofIsValid += 1
                
            if countQtdDataNecessaryToProofIsValid >= 2:
                isPagamento = True

            data = str(data)
            dataSplit = data.split(':')

            fieldOne = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 1))
            fieldTwo = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 2))
            # fieldThree = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 3))
            
            if fieldOne == 'CONTA':
                account = funcoesUteis.treatNumberField(fieldTwo.split('/')[0])

            if fieldOne.count('NOME') > 0 and fieldOne.count("BENEFICIARIO") > 0:
                nameProvider = fieldTwo

            if fieldOne.count('CNPJ') > 0 and fieldOne.count("BENEFICIARIO") > 0:
                cgceProvider = fieldTwo

            if fieldOne.count('CNPJ') > 0 and fieldOne.count("PAGADOR") > 0:
                cgcePaying = fieldTwo

            if fieldOne == "DATA PAGAMENTO":
                paymentDate = funcoesUteis.retornaCampoComoData(fieldTwo)

            if fieldOne == "DATA VENCIMENTO":
                dueDate = funcoesUteis.retornaCampoComoData(fieldTwo)

            if fieldOne == "VALOR DOCUMENTO":
                amountOriginal = funcoesUteis.treatDecimalField(fieldTwo)

            if fieldOne.count('DESCONTO') > 0 and fieldOne.count("ABATIMENTO") > 0:
                amountDiscount = funcoesUteis.treatDecimalField(fieldTwo)

            if fieldOne.count('OUTROS ACRESCIMOS') > 0:
                amountInterest = funcoesUteis.treatDecimalField(fieldTwo)

            if fieldOne == "VALOR PAGO":
                amountPaid = funcoesUteis.treatDecimalField(fieldTwo)            

            if fieldOne == "VALOR PAGO":
                if paymentDate is not None and amountPaid > 0 and isPagamento is True:
                    valuesOfLine = {
                        "paymentDate": paymentDate,
                        "nameProvider": nameProvider,
                        "cgceProvider": cgceProvider,
                        "dueDate": dueDate,
                        "bank": 'SICOOB',
                        "account": account,
                        "amountPaid": round(amountPaid, 2),
                        "amountInterest": round(amountInterest, 2),
                        "amountDiscount": round(amountDiscount, 2),
                        "amountFine": round(amountFine, 2),
                        "amountOriginal": round(amountOriginal, 2),
                        "historic": historic,
                        "category": '',
                        "cgcePaying": cgcePaying,
                        "foundProof": True,
                        "amountPaidPerLote": round(amountPaid, 2),
                        "wayFile": self._file
                    }

                    valuesOfFile.append(valuesOfLine.copy())

        return valuesOfFile