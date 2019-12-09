import sys
import os

fileDir = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(os.path.join(fileDir, 'backend'))

import json
from tools.leArquivos import leXls_Xlsx, leTxt
import tools.funcoesUteis as funcoesUteis


class ProofsPaymentsItau(object):

    def __init__(self, file):
        self._valuesOfLine = {}
        self._valuesOfFile = []
        # possíveis textos que a linha de pagamento começa, exemplo: TRANSFERENCIA REALIZADA EM 19.09.2019
        self._valuesOfLinePayments = ["PAGAMENTO EFETUADO EM", "TRANSFERENCIA REALIZADA EM", "TRANSFERENCIA EFETUADA EM", "PAGAMENTO REALIZADO EM", \
            "OPERACAO EFETUADA EM", "TED SOLICITADA EM"]
        self._file = file
        self._dataFile = leTxt(file, treatAsText=True, removeBlankLines=True)

    def process(self):

        nameProvider = ""
        namePayee = ""
        historic = ""
        dueDate = None
        company = ""
        cnpjProvider = ""
        amountPaid = float(0)

        for key, data in enumerate(self._dataFile):

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
                bank = f"ITAU - {self._dataFile[key+1]}"

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
                            "company": company,
                            "foundProof": True
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

class SispagItauExcel(object):

    def __init__(self, file):
        self._file = file
        self._dataFile = leXls_Xlsx(self._file)
        self._valuesOfLine = {}
        self._valuesOfFile = []
        self._posionsOfHeader = {}

    def isSispagItauExcel(self):
        for data in self._dataFile:
            fieldOne = funcoesUteis.treatTextFieldInVector(data, 1)
            fieldTwo = funcoesUteis.treatTextFieldInVector(data, 2)
            fieldThree = funcoesUteis.treatTextFieldInVector(data, 3)

            if fieldOne == "NOME DO FAVORECIDO" and fieldTwo == "CPF/CNPJ" and fieldThree == "TIPO DE PAGAMENTO":
                return True

    def process(self):
        bank = ""
        for data in self._dataFile:
            try:
                fieldOne = funcoesUteis.treatTextFieldInVector(data, 1)

                if fieldOne.count('NOME DO FAVORECIDO') > 0:
                    self._posionsOfHeader.clear()
                    for keyField, nameField in enumerate(data):
                        nameField = funcoesUteis.treatTextField(nameField)
                        self._posionsOfHeader[nameField] = keyField

                if fieldOne == "AGENCIA/CONTA:":
                    agencyAndAccount = funcoesUteis.treatTextFieldInVector(data, 2)
                    bankSplit = agencyAndAccount.split('/')
                    try:
                        account = funcoesUteis.treatNumberField(bankSplit[1][:-1]) # o -1 é pq o último digíto é o verificador, e nem sempre no extrato tem ele
                    except Exception:
                        account = ""
                    
                    bank = "ITAU" 

                paymentDate = funcoesUteis.treatDateFieldInVector(data, fieldsHeader=self._posionsOfHeader, nameFieldHeader="Data de pagamento")

                nameProvider = funcoesUteis.treatTextFieldInVector(data, fieldsHeader=self._posionsOfHeader, nameFieldHeader="Nome do favorecido")

                amountPaid = funcoesUteis.treatDecimalFieldInVector(data, fieldsHeader=self._posionsOfHeader, nameFieldHeader="Valor do Pagamento (R$)")

                cnpjProvider = funcoesUteis.treatNumberFieldInVector(data, fieldsHeader=self._posionsOfHeader, nameFieldHeader="CPF/CNPJ")

                if paymentDate is not None and amountPaid > 0:
                    self._valuesOfLine = {
                        "paymentDate": funcoesUteis.transformaCampoDataParaFormatoBrasileiro(paymentDate),
                        "nameProvider": nameProvider,
                        "cnpjProvider": cnpjProvider,
                        "amountPaid": amountPaid,
                        "bank": bank,
                        "account": account
                    }

                    self._valuesOfFile.append(self._valuesOfLine.copy())

            except Exception as e:
                print(e)

        return self._valuesOfFile

if __name__ == "__main__":
    # proofsPaymentsItau = ProofsPaymentsItau("C:/_temp/integracao_diviart/CONTASANGIOTOMO092019-PAGINA 14-PAGINA 1.tmp")
    # print(proofsPaymentsItau.process())

    sispagItauExcel = SispagItauExcel("C:/integracao_contabil/1428/arquivos_originais/Sispag detalhada.xlsx")
    print(sispagItauExcel.process())
            