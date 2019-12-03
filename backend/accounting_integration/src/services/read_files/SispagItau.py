import sys
import os

fileDir = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(os.path.join(fileDir, 'backend'))

import json
from tools.leArquivos import leXls_Xlsx, leTxt
import tools.funcoesUteis as funcoesUteis


class SispagItau(object):

    def __init__(self):
        self._valuesOfLine = {}
        self._valuesOfFile = []
        # possíveis textos que a linha de pagamento começa, exemplo: TRANSFERENCIA REALIZADA EM 19.09.2019
        self._valuesOfLinePayments = ["PAGAMENTO EFETUADO EM", "TRANSFERENCIA REALIZADA EM", "TRANSFERENCIA EFETUADA EM", "PAGAMENTO REALIZADO EM", \
            "OPERACAO EFETUADA EM", "TED SOLICITADA EM"]

    def process(self, file):
        dataFile = leTxt(file, treatAsText=True, removeBlankLines=True)

        nameProvider = ""
        namePayee = ""
        historic = ""
        dueDate = None
        company = ""
        cnpjProvider = ""
        amountPaid = float(0)

        for key, data in enumerate(dataFile):

            data = str(data)
            dataSplit = data.split(':')

            try:
                fieldOne = dataSplit[0]
            except Exception:
                fieldOne = ""

            try:
                fieldTwo = dataSplit[1].strip()
            except Exception:
                fieldTwo = ""

            if fieldOne == "NOME":
                nameProvider = funcoesUteis.treatTextField(fieldTwo)

            if fieldOne == "NOME DO FAVORECIDO":
                nameProvider = funcoesUteis.treatTextField(fieldTwo)
                namePayee = nameProvider
            
            if fieldOne.count("GUIA DE RECOLHIMENTO") > 0:
                historic = funcoesUteis.treatTextField(data)
                
            if fieldOne == "INFORMACOES FORNECIDAS PELO PAGADOR":
                historic = funcoesUteis.treatTextField(fieldTwo)
			
            if fieldOne == "DATA DE VENCIMENTO":
                dueDate = funcoesUteis.transformaCampoDataParaFormatoBrasileiro(funcoesUteis.retornaCampoComoData(fieldTwo))

            if ( fieldOne.count("CPF") > 0 or fieldOne.count("CNPJ") > 0 ) and fieldOne.count("PAGADOR") > 0:
                company = funcoesUteis.treatNumberField(fieldTwo)

            if ( fieldOne.count("CPF") > 0 or fieldOne.count("CNPJ") > 0 ) and fieldOne.count("PAGADOR") == 0:
                cnpjProvider = funcoesUteis.treatNumberField(fieldTwo)

            if fieldOne.count("VALOR") > 0:
                amountPaid = funcoesUteis.treatDecimalField(fieldTwo)

            if fieldOne.count("CONTA") > 0 and fieldOne.count("DEBITADA") > 0:
                bank = f"ITAU - {dataFile[key+1]}"

			# quando é pagamento de imposto não tem o nome do fornecedor, o dados vem na informação complementar
            if historic != "" and dueDate == "" and namePayee == "":
                nameProvider = historic

            for valueOfLinePayment in self._valuesOfLinePayments:
                if data[0 : len(valueOfLinePayment) ] == valueOfLinePayment:
                    paymentDate = funcoesUteis.treatTextField(data[len(valueOfLinePayment)+1:len(valueOfLinePayment)+11])
                    paymentDate = funcoesUteis.retornaCampoComoData(paymentDate.replace('.', '/'))

                    if paymentDate is not None and amountPaid > 0:
                        self._valuesOfLine = {
                            "paymentDate": funcoesUteis.transformaCampoDataParaFormatoBrasileiro(paymentDate),
                            "nameProvider": nameProvider,
                            "cnpjProvider": cnpjProvider,
                            "dueDate": dueDate,
                            "bank": bank,
                            "amountPaid": amountPaid,
                            "amountDiscount": float(0),
                            "amountInterest": float(0),
                            "amountOriginal": float(0),
                            "historic": historic,
                            "company": company
                        }

                        self._valuesOfFile.append(self._valuesOfLine.copy())
                    
                    nameProvider = ""
                    namePayee = ""
                    historic = ""
                    dueDate = None
                    company = ""
                    cnpjProvider = ""
                    amountPaid = float(0)

                    break

        return self._valuesOfFile

if __name__ == "__main__":
    sispagItau = SispagItau()
    print(sispagItau.process("C:/_temp/integracao_diviart/CONTASANGIOTOMO092019-PAGINA 14-PAGINA 1.tmp"))
            