import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import tools.funcoesUteis as funcoesUteis

class Pix(object):
    def __init__(self, dataFile):
        self._dataFile = dataFile
        self._valuesOfLineDatePayment = ["PAGAMENTO EFETUADO EM", "PAGAMENTO REALIZADO EM", "OPERACAO EFETUADA EM"]
        self._typeLineRead = ''

    def process(self):
        valuesOfLine = {}

        isProofFileThisClass = False

        nameProvider = ""
        cgceProvider = ""
        historic = ""
        amountPaid = float(0)
        account = ""
        dueDate = None
        amountOriginal = float(0)
        amountDiscount = float(0)
        amountInterest = float(0)
        paymentDate = None
        
        for data in self._dataFile:
            # if isProofFileThisClass == False and data.find('TIPO DE PAGAMENTO PIX') >= 0:
            #     isProofFileThisClass = True

            data = str(data)
            dataSplitTwoPoints = data.split(':')

            fieldOne = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplitTwoPoints, 1))
            fieldTwo = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplitTwoPoints, 2))

            if data.find('DADOS DO PAGADOR') >= 0:
                self._typeLineRead = 'PAGADOR'
            elif data.find('DADOS DO RECEBEDOR') >= 0:
                self._typeLineRead = 'RECEBEDOR'
            elif data.find('DADOS DA TRANSACAO') >= 0:
                self._typeLineRead = 'TRANSACAO'

            if self._typeLineRead == 'PAGADOR':
                if fieldOne.count('AGENCIA/CONTA') > 0:
                    account = funcoesUteis.analyzeIfFieldIsValidMatrix(fieldTwo.split('/'), 2)
                    account = str(funcoesUteis.treatNumberField(account))
                    
                if fieldOne.count('CPF / CNPJ') > 0:
                    cgcePaying = fieldTwo
            elif self._typeLineRead == 'RECEBEDOR':
                if fieldOne == "NOME DO RECEBEDOR":
                    nameProvider = fieldTwo
                
                if fieldOne.count('CPF / CNPJ') > 0:
                    cgceProvider = funcoesUteis.treatNumberField(fieldTwo)
                
            elif self._typeLineRead == 'TRANSACAO':
                if fieldOne == "VALOR":
                    amountPaid = funcoesUteis.treatDecimalField(fieldTwo)
                
                if fieldOne.count('DATA DA TRANSF') > 0:
                    paymentDate = funcoesUteis.retornaCampoComoData(fieldTwo)            

            if fieldOne.count('TIPO DE PAGAMENTO') > 0:
                # print(fieldOne, fieldTwo, paymentDate, amountPaid, isProofFileThisClass)
                if paymentDate is not None and amountPaid > 0:
                    valuesOfLine = {
                        "paymentDate": paymentDate,
                        "nameProvider": nameProvider,
                        "cgceProvider": cgceProvider,
                        "dueDate": dueDate,
                        "bank": 'ITAU',
                        "account": account,
                        "amountPaid": round(amountPaid, 2),
                        "amountInterest": round(amountInterest, 2),
                        "amountDiscount": round(amountDiscount, 2),
                        "amountOriginal": round(amountOriginal, 2),
                        "historic": historic,
                        "category": 'PIX',
                        "cgcePaying": cgcePaying,
                        "foundProof": True,
                        "amountPaidPerLote": round(amountPaid, 2)
                    }

                    return valuesOfLine.copy()

            