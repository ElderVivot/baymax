import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import tools.funcoesUteis as funcoesUteis

class Agendamento(object):
    def __init__(self, dataFile):
        self._dataFile = dataFile
        self._valuesOfLineDatePayment = ["AGENDAMENTO EFETUADO EM"]
        self._typeLineRead = ''

    def process(self):
        valuesOfLine = {}

        isProofAgendamento = False

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
            if isProofAgendamento == False and data.find('COMPROVANTE DE AGENDAMENTO') >= 0:
                isProofAgendamento = True

            data = str(data)
            dataSplit = data.split(':')

            fieldOne = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 1))
            fieldTwo = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 2))

            # faço esta separação pra poder identificar o que deve ser lido, pois os dados estão na linha abaixo e não onde 'BENEFICIARIO' por exemplo
            if fieldOne.count('CONTA A SER DEBITADA') > 0:
                self._typeLineRead = 'conta_debitada'
            elif fieldOne.count('DADOS DO PAGAMENTO') > 0:
                self._typeLineRead = 'dados_pagamento'
            elif fieldOne.count('DADOS DO BENEFICIARIO') > 0:
                self._typeLineRead = 'beneficiario'
            elif fieldOne.count('DADOS DO PAGADOR') > 0:
                self._typeLineRead = 'pagador'
            elif fieldOne.count('DADOS DO BOLETO') > 0:
                self._typeLineRead = 'dados_boleto'

            if self._typeLineRead == "conta_debitada":
                if fieldOne.count('AGENCIA') > 0:
                    account = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 3))
                    account = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(account.split('-'), 1))
                    if account.find(' ') > 0:
                        account = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(account.split(' '), 1))
            if self._typeLineRead == 'beneficiario':
                if fieldOne == "NOME":
                    nameProvider = fieldTwo
                if fieldOne == "RAZAO SOCIAL":
                    nameProvider = fieldTwo
                if fieldOne.count('CNPJ') > 0 or fieldOne.count('CPF') > 0:
                    cgceProvider = funcoesUteis.treatNumberField(fieldTwo)
            if self._typeLineRead == 'pagador':
                if fieldOne.count('CNPJ') > 0 or fieldOne.count('CPF') > 0:
                    cgcePaying = funcoesUteis.treatNumberField(fieldTwo)
            elif self._typeLineRead == 'dados_boleto':
                if fieldOne == "DATA DE VENCIMENTO":
                    dueDate = funcoesUteis.retornaCampoComoData(fieldTwo)
                if fieldOne == "DATA DO PAGAMENTO":
                    paymentDate = funcoesUteis.retornaCampoComoData(fieldTwo)
                if fieldOne == "VALOR DO DOCUMENTO":
                    amountOriginal = funcoesUteis.treatDecimalField(fieldTwo)
                if fieldOne == "DESCONTO":
                    amountDiscount = funcoesUteis.treatDecimalField(fieldTwo)
                if fieldOne == "JUROS/MORA":
                    amountInterest = funcoesUteis.treatDecimalField(fieldTwo)
                if fieldOne == "MULTA":
                    amountFine = funcoesUteis.treatDecimalField(fieldTwo)
                if fieldOne == "VALOR DO PAGAMENTO":
                    amountPaid = funcoesUteis.treatDecimalField(fieldTwo)            

            for valueOfLineDatePayment in self._valuesOfLineDatePayment:
                if data[0 : len(valueOfLineDatePayment) ] == valueOfLineDatePayment:
                    if paymentDate is None: # apenas se for None, pq o de agendamento tem um campo especifico pra data
                        paymentDate = funcoesUteis.treatTextField(data[len(valueOfLineDatePayment)+1:len(valueOfLineDatePayment)+11])
                        if paymentDate.find('.') >= 0:
                            paymentDate = funcoesUteis.retornaCampoComoData(paymentDate.replace('.', '/'))
                        else:
                            paymentDate = funcoesUteis.retornaCampoComoData(paymentDate)  

                    if paymentDate is not None and amountPaid > 0 and isProofAgendamento is True:
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
                            "amountFine": round(amountFine, 2),
                            "amountOriginal": round(amountOriginal, 2),
                            "historic": historic,
                            "category": 'AGENDAMENTO',
                            "cgcePaying": cgcePaying,
                            "foundProof": True,
                            "amountPaidPerLote": round(amountPaid, 2)
                        }

                        return valuesOfLine.copy()

            