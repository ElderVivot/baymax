import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import tools.funcoesUteis as funcoesUteis

class TedC(object):
    def __init__(self, dataFile, file):
        self._dataFile = dataFile
        self._file = file
        self._valuesOfLineDatePayment = ["TED SOLICITADA EM"]
        self._accountDebitOrCredit = ''

    def process(self):
        valuesOfLine = {}

        isProofTEDC = False

        nameProvider = ""
        cgceProvider = ""
        historic = ""
        amountPaid = float(0)
        account = ""
        
        for data in self._dataFile:
            if isProofTEDC == False and data.find('TED C') >= 0:
                isProofTEDC = True

            data = str(data)
            dataSplit = data.split(':')

            fieldOne = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 1))
            fieldTwo = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 2))

            if fieldOne.count('IDENTIFICACAO NO EXTRATO') > 0:
                historic = funcoesUteis.treatTextField(fieldTwo)

            if fieldOne.count('CONTA DEBITADA') > 0:
                self._accountDebitOrCredit = 'DEBIT'
            elif fieldOne.count('DADOS DA TED') > 0:
                self._accountDebitOrCredit = 'CREDIT'

            if self._accountDebitOrCredit == 'DEBIT':
                if fieldOne.count('AGENCIA') > 0:
                    account = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 3))
                    account = str(funcoesUteis.treatNumberField(account))
                    # account = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(account.split('-'), 1))
                    # if account.find(' ') > 0:
                    #     account = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(account.split(' '), 1))
            elif self._accountDebitOrCredit == 'CREDIT':
                if fieldOne.count("NOME DO FAVORECIDO") > 0:
                    nameProvider = fieldTwo

                if fieldOne.count("CNPJ") > 0:
                    cgceProvider = fieldTwo

                if fieldOne.count("VALOR DA TED") > 0:
                    amountPaid = funcoesUteis.treatDecimalField(fieldTwo)

            for valueOfLineDatePayment in self._valuesOfLineDatePayment:
                if data[0 : len(valueOfLineDatePayment) ] == valueOfLineDatePayment:
                    paymentDate = funcoesUteis.treatTextField(data[len(valueOfLineDatePayment)+1:len(valueOfLineDatePayment)+11])
                    if paymentDate.find('.') >= 0:
                        paymentDate = funcoesUteis.retornaCampoComoData(paymentDate.replace('.', '/'))
                    else:
                        paymentDate = funcoesUteis.retornaCampoComoData(paymentDate)

                    if paymentDate is not None and amountPaid > 0 and isProofTEDC is True:
                        valuesOfLine = {
                            "paymentDate": paymentDate,
                            "nameProvider": nameProvider,
                            "cgceProvider": cgceProvider,
                            "dueDate": '',
                            "bank": 'ITAU',
                            "account": account,
                            "amountPaid": round(amountPaid, 2),
                            "historic": historic,
                            "category": 'TED C',
                            "cgcePaying": '',
                            "foundProof": True,
                            "amountPaidPerLote": round(amountPaid, 2),
                            "wayFile": self._file
                        }

                        return valuesOfLine.copy()

            