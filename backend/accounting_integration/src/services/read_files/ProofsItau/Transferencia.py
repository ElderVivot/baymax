import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import tools.funcoesUteis as funcoesUteis

class Transferencia(object):
    def __init__(self, dataFile):
        self._dataFile = dataFile
        self._valuesOfLineDatePayment = ["TRANSFERENCIA REALIZADA EM", "TRANSFERENCIA EFETUADA EM", "OPERACAO EFETUADA EM", "TED SOLICITADA EM"]
        self._accountDebitOrCredit = ''

    def process(self):
        valuesOfLine = {}

        isProofTransferencia = False

        nameProvider = ""
        historic = ""
        amountPaid = float(0)
        account = ""
        
        for data in self._dataFile:
            if isProofTransferencia == False and data.find('COMPROVANTE DE TRANSFERENCIA') >= 0:
                isProofTransferencia = True

            data = str(data)
            dataSplit = data.split(':')

            fieldOne = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 1))
            fieldTwo = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 2))

            if fieldOne.count('IDENTIFICACAO NO EXTRATO') > 0:
                historic = funcoesUteis.treatTextField(fieldTwo)

            if fieldOne.count('CONTA DEBITADA') > 0:
                self._accountDebitOrCredit = 'DEBIT'
            elif fieldOne.count('CONTA CREDITADA') > 0:
                self._accountDebitOrCredit = 'CREDIT'

            if self._accountDebitOrCredit == 'DEBIT':
                if fieldOne.count('AGENCIA') > 0:
                    account = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 3))
                    account = str(funcoesUteis.treatNumberField(account))
                    # account = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(account.split('-'), 1))
                    # if account.find(' ') > 0:
                    #     account = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(account.split(' '), 1))
            elif self._accountDebitOrCredit == 'CREDIT':
                if fieldOne == "NOME":
                    nameProvider = fieldTwo

                if fieldOne.count("VALOR") > 0:
                    amountPaid = funcoesUteis.treatDecimalField(fieldTwo)

            for valueOfLineDatePayment in self._valuesOfLineDatePayment:
                if data[0 : len(valueOfLineDatePayment) ] == valueOfLineDatePayment:
                    paymentDate = funcoesUteis.treatTextField(data[len(valueOfLineDatePayment)+1:len(valueOfLineDatePayment)+11])
                    if paymentDate.find('.') >= 0:
                        paymentDate = funcoesUteis.retornaCampoComoData(paymentDate.replace('.', '/'))
                    else:
                        paymentDate = funcoesUteis.retornaCampoComoData(paymentDate)  

                    if paymentDate is not None and amountPaid > 0 and isProofTransferencia is True:
                        valuesOfLine = {
                            "paymentDate": paymentDate,
                            "nameProvider": nameProvider,
                            "cgceProvider": '',
                            "dueDate": '',
                            "bank": 'ITAU',
                            "account": account,
                            "amountPaid": round(amountPaid, 2),
                            "historic": historic,
                            "category": 'TRANSFERENCIA',
                            "cgcePaying": '',
                            "foundProof": True,
                            "amountPaidPerLote": round(amountPaid, 2)
                        }

                        return valuesOfLine.copy()

            