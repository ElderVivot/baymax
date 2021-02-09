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
            if data.find('COMPROVANTE DE TRANSACAO BANCARIA') >= 0:
                countQtdDataNecessaryToProofIsValid = 0
                countQtdDataNecessaryToProofIsValid += 1

            if data.find('TRANSACAO ACIMA FOI REALIZADA') >= 0:
                countQtdDataNecessaryToProofIsValid += 1
                
            if countQtdDataNecessaryToProofIsValid >= 2:
                isPagamento = True

            data = str(data)
            dataSplit = data.split(':')

            fieldOne = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 1))
            fieldTwo = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 2))
            # fieldThree = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 3))
            
            if fieldOne == 'CONTA DE DEBITO':
                account = funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 4)
                account = account.split('|')
                account = funcoesUteis.analyzeIfFieldIsValidMatrix(account, 1)
                account = account.split('-')
                account = funcoesUteis.treatNumberFieldInVector(account, 1, isInt=True)
                account = str(account)

            if data.count('RAZAO SOCIAL') > 0 and data.count('SACADOR') == 0:
                positionRazaoSocial = data.find('RAZAO SOCIAL') + len('RAZAO SOCIAL')
                nameProvider = funcoesUteis.treatTextField(data[positionRazaoSocial:])

            if fieldOne.count('CNPJ') > 0 and fieldOne.count("BENEFICIARIO") > 0:
                cgceProvider = fieldTwo

            if fieldOne.count('CNPJ') > 0 and fieldOne.count("PAGADOR") > 0:
                cgcePaying = fieldTwo

            if fieldOne == "DATA DE DEBITO":
                paymentDate = funcoesUteis.retornaCampoComoData(fieldTwo)

            if fieldOne == "DATA DE VENCIMENTO":
                dueDate = funcoesUteis.retornaCampoComoData(fieldTwo)

            if fieldOne == "VALOR":
                amountOriginal = funcoesUteis.treatDecimalField(fieldTwo, decimalSeparator='.')

            if fieldOne.count('DESCONTO') > 0:
                amountDiscount = funcoesUteis.treatDecimalField(fieldTwo, decimalSeparator='.')

            if fieldOne.count('MULTA') > 0:
                amountFine = funcoesUteis.treatDecimalField(fieldTwo, decimalSeparator='.')

            if fieldOne.count('JUROS') > 0:
                amountInterest = funcoesUteis.treatDecimalField(fieldTwo, decimalSeparator='.')

            if fieldOne == "VALOR TOTAL":
                amountPaid = funcoesUteis.treatDecimalField(fieldTwo, decimalSeparator='.')

            if fieldOne == "DESCRICAO":
                historic = funcoesUteis.treatDecimalField(fieldTwo)            

            if data.find('TRANSACAO ACIMA FOI REALIZADA') >= 0:
                if paymentDate is not None and amountPaid > 0 and isPagamento is True:
                    valuesOfLine = {
                        "paymentDate": paymentDate,
                        "nameProvider": nameProvider,
                        "cgceProvider": cgceProvider,
                        "dueDate": dueDate,
                        "bank": 'BRADESCO',
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