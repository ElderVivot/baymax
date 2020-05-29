import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import tools.funcoesUteis as funcoesUteis

class DefaultSispag(object):
    def __init__(self, dataFile):
        self._dataFile = dataFile
        self._valuesOfLineDatePayment = ["PAGAMENTO EFETUADO EM", "TRANSFERENCIA REALIZADA EM", "TRANSFERENCIA EFETUADA EM", "PAGAMENTO REALIZADO EM", \
            "OPERACAO EFETUADA EM", "TED SOLICITADA EM"]
        self._accountDebitOrCredit = ''

    def process(self):
        valuesOfLine = {}

        isProofDefaultSispag = False

        nameProvider = ""
        namePayee = ""
        historic = ""
        dueDate = None
        cgcePaying = ""
        cnpjProvider = ""
        amountPaid = float(0)
        category = ""
        bank = "ITAU"
        account = ""

        for data in self._dataFile:

            data = str(data)
            dataSplit = data.split(':')

            fieldOne = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 1))

            fieldTwo = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 2))

            if fieldOne.count('COMPROVANTE DE OPERACAO') > 0:
                category = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(data.split('-'), 2))
            if fieldOne.count('PAGAMENTO COM CODIGO DE BARRAS') > 0:
                category = 'PAGTO COD BARRA'
            if fieldOne.count("PAGAMENTO DE CONCESSIONARIAS") > 0:
                category = 'PAGTO CONCESSIONARIA'
            if fieldOne.count("FGTS") > 0 or fieldOne.count("GRRF") > 0:
                category = 'PAGTO FGTS-GRRF'
            if fieldOne.count("GUIA DE RECOLHIMENTO") > 0:
                category = 'PAGTO GRF'
                historic = funcoesUteis.treatTextField(data)
            
            if fieldOne.count("IDENTIFICACAO NO EXTRATO") > 0:
                historic = fieldTwo

            if fieldOne.count('CONTA') > 0 and fieldOne.count('DEBITADA') > 0:
                self._accountDebitOrCredit = 'DEBIT'
            elif fieldOne.count('CONTA A SER CREDITADA') > 0 or fieldOne.count('DADOS DO PAGAMENTO') > 0:
                self._accountDebitOrCredit = 'CREDIT'

            if self._accountDebitOrCredit == 'DEBIT':
                if fieldOne.count('AGENCIA') > 0:
                    account = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 3))
                    account = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(account.split('-'), 1))
                    if account.find(' ') > 0:
                        account = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(account.split(' '), 1))
            elif self._accountDebitOrCredit == 'CREDIT':
                if fieldOne == "NOME":
                    nameProvider = fieldTwo

                if fieldOne == "NOME DO FAVORECIDO":
                    nameProvider = fieldTwo
                    namePayee = nameProvider
                    
                if fieldOne == "INFORMACOES FORNECIDAS PELO PAGADOR":
                    historic = fieldTwo
                
                if fieldOne == "DATA DE VENCIMENTO":
                    dueDate = funcoesUteis.transformaCampoDataParaFormatoBrasileiro(funcoesUteis.retornaCampoComoData(fieldTwo))

                if ( fieldOne.count("CPF") > 0 or fieldOne.count("CNPJ") > 0 ) and fieldOne.count("PAGADOR") > 0:
                    cgcePaying = funcoesUteis.treatNumberField(fieldTwo)

                if ( fieldOne.count("CPF") > 0 or fieldOne.count("CNPJ") > 0 ) and fieldOne.count("PAGADOR") == 0:
                    cnpjProvider = funcoesUteis.treatNumberField(fieldTwo)

                if fieldOne.count("VALOR") > 0:
                    amountPaid = funcoesUteis.treatDecimalField(fieldTwo)

			# quando é pagamento de imposto não tem o nome do fornecedor, o dados vem na informação complementar
            if historic != "" and dueDate == "" and namePayee == "":
                nameProvider = historic

            # se o nome do fornecedor ainda for vazio, então considero a categoria como fornecedor
            if nameProvider == "" and category != "":
                nameProvider = category

            for valueOfLineDatePayment in self._valuesOfLineDatePayment:
                if data[0 : len(valueOfLineDatePayment) ] == valueOfLineDatePayment:
                    paymentDate = funcoesUteis.treatTextField(data[len(valueOfLineDatePayment)+1:len(valueOfLineDatePayment)+11])
                    paymentDate = funcoesUteis.retornaCampoComoData(paymentDate.replace('.', '/'))

                    if paymentDate is not None and amountPaid > 0:
                        valuesOfLine = {
                            "paymentDate": paymentDate,
                            "nameProvider": nameProvider,
                            "cgceProvider": cnpjProvider,
                            "dueDate": dueDate,
                            "bank": bank,
                            "account": account,
                            "amountPaid": round(amountPaid, 2),
                            "historic": historic,
                            "category": category,
                            "cgcePaying": cgcePaying,
                            "foundProof": True,
                            "amountPaidPerLote": round(amountPaid, 2)
                        }

                        return valuesOfLine.copy()

            