import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import tools.funcoesUteis as funcoesUteis

class PagamentoBoleto(object):
    def __init__(self, dataFile):
        self._dataFile = dataFile
        self._valuesOfLineDatePayment = ["PAGAMENTO EFETUADO EM", "PAGAMENTO REALIZADO EM", "OPERACAO EFETUADA EM"]
        self._typeLineRead = ''

    def process(self):
        valuesOfLine = {}

        isProofPagamentoBoleto = False

        nameProvider = ""
        cgceProvider = ""
        historic = ""
        amountPaid = float(0)
        account = ""
        dueDate = None
        amountOriginal = float(0)
        amountDiscount = float(0)
        amountInterest = float(0)
        
        for data in self._dataFile:
            if isProofPagamentoBoleto == False and data.find('PAGAMENTO DE BOLETO') >= 0:
                isProofPagamentoBoleto = True

            data = str(data)
            dataSplitTwoPoints = data.split(':')
            dataSplitSpace = data.split(' ')

            fieldOne = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplitTwoPoints, 1))
            fieldTwo = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplitTwoPoints, 2))

            if fieldOne.count('AGENCIA/CONTA') > 0:
                account = funcoesUteis.analyzeIfFieldIsValidMatrix(fieldTwo.split('/'), 2)
                account = str(funcoesUteis.treatNumberField(account))
                # account = str(funcoesUteis.treatNumberField(funcoesUteis.analyzeIfFieldIsValidMatrix(account.split('-'), 1), isInt=True))

                cgcePaying = funcoesUteis.treatNumberField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplitTwoPoints, 3))
            
            # faço esta separação pra poder identificar o que deve ser lido, pois os dados estão na linha abaixo e não onde 'BENEFICIARIO' por exemplo
            if fieldOne == 'BENEFICIARIO':
                self._typeLineRead = 'beneficiario'
            elif fieldOne.count('VALOR DO BOLETO') > 0 or fieldOne.count('VALOR DO DOCUMENTO') > 0:
                self._typeLineRead = 'valor_boleto'
            elif fieldOne.count('DESCONTO') > 0 and fieldOne.count('(-)') > 0:
                self._typeLineRead = 'desconto'
            elif fieldOne.count('MORA/MULTA') > 0 and fieldOne.count('(+)') > 0:
                self._typeLineRead = 'juros'
            if data.count('VALOR DO PAGAMENTO') > 0 and data.count('R$') > 0:
                self._typeLineRead = 'valor_pago'
            elif data.count('DATA DE PAGAMENTO') > 0:
                self._typeLineRead = 'data_pagamento'

            # dados da linha do BENEFICIARIO
            if self._typeLineRead == 'beneficiario' and fieldOne.count('BENEFICIARIO') == 0:
                # alguns comprovantes de boleto tem a RAZAO SOCIAL e CNPJ também
                if(fieldOne == "RAZAO SOCIAL"):
                    nameProvider = ' '.join(dataSplitSpace[2:len(dataSplitSpace)-2])
                    cgceProvider = funcoesUteis.treatNumberField(dataSplitSpace[len(dataSplitSpace)-2])
                else:
                    nameProvider = ' '.join(dataSplitSpace[:len(dataSplitSpace)-1])
                
                nameProvider = nameProvider.strip()
                dueDate = funcoesUteis.retornaCampoComoData(dataSplitSpace[len(dataSplitSpace)-1])
            # dados da linha do VALOR ORIGINAL DO BOLETO
            elif self._typeLineRead == 'valor_boleto' and fieldOne.count('VALOR DO BOLETO') == 0 and fieldOne.count('VALOR DO DOCUMENTO') == 0:
                amountOriginal = funcoesUteis.treatDecimalField(dataSplitSpace[len(dataSplitSpace)-1])
            # dados da linha do VALOR DESCONTO
            elif self._typeLineRead == 'desconto' and fieldOne.count('DESCONTO') == 0:
                amountDiscount = funcoesUteis.treatDecimalField(dataSplitSpace[len(dataSplitSpace)-1])
            # dados da linha do VALOR MORA/MULTA
            elif self._typeLineRead == 'juros' and fieldOne.count('MORA/MULTA') == 0:
                amountInterest = funcoesUteis.treatDecimalField(dataSplitSpace[len(dataSplitSpace)-1])
            # dados da linha do VALOR MORA/MULTA
            elif self._typeLineRead == 'valor_pago' and data.count('VALOR DO PAGAMENTO') == 0 and data.count('R$') == 0:
                amountPaid = funcoesUteis.treatDecimalField(dataSplitSpace[len(dataSplitSpace)-1])

            for valueOfLineDatePayment in self._valuesOfLineDatePayment:
                if data[0 : len(valueOfLineDatePayment) ] == valueOfLineDatePayment:
                    paymentDate = funcoesUteis.treatTextField(data[len(valueOfLineDatePayment)+1:len(valueOfLineDatePayment)+11])
                    if paymentDate.find('.') >= 0:
                        paymentDate = funcoesUteis.retornaCampoComoData(paymentDate.replace('.', '/'))
                    else:
                        paymentDate = funcoesUteis.retornaCampoComoData(paymentDate)  

                    if paymentDate is not None and amountPaid > 0 and isProofPagamentoBoleto is True:
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
                            "category": 'PAGTO DE BOLETO',
                            "cgcePaying": cgcePaying,
                            "foundProof": True,
                            "amountPaidPerLote": round(amountPaid, 2)
                        }

                        return valuesOfLine.copy()

            