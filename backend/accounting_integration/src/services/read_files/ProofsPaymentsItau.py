import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import json
from tools.leArquivos import leXls_Xlsx, leTxt, readJson
import tools.funcoesUteis as funcoesUteis
from rules.ReturnFilesDontFindForm import ReturnFilesDontFindForm


class ProofsPaymentsItau(object):

    def __init__(self, wayTemp):
        self._proofs = []
        # possíveis textos que a linha de pagamento começa, exemplo: TRANSFERENCIA REALIZADA EM 19.09.2019
        self._valuesOfLinePayments = ["PAGAMENTO EFETUADO EM", "TRANSFERENCIA REALIZADA EM", "TRANSFERENCIA EFETUADA EM", "PAGAMENTO REALIZADO EM", \
            "OPERACAO EFETUADA EM", "TED SOLICITADA EM"]
        self._wayTemp = wayTemp
        self._wayTempFilesRead = os.path.join(wayTemp, 'FilesReads.json')
        self._accountDebitOrCredit = ''

        # deleta os arquivos da pasta temp que já tenham sido processados, pra não processar duas vezes
        returnFilesDontFindForm = ReturnFilesDontFindForm(0, self._wayTemp)
        returnFilesDontFindForm.removeAlreadyProcessed()

    def isProofOfItau(self, file):
        dataFile = leTxt(file, treatAsText=True, removeBlankLines=True)
        countProofOfItau = 0
        for data in dataFile:
            data = str(data)
            dataSplit = data.split(':')

            fieldOne = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 1))
            if fieldOne.count('COMPROVANTE DE OPERACAO') > 0:
                countProofOfItau += 1
            if fieldOne.count('CONTA A SER DEBITADA') > 0:
                countProofOfItau += 1
            if countProofOfItau == 2:
                return True

    def process(self, file):
        # se não for desta classe nem segue pra frente
        if self.isProofOfItau(file) is None:
            return []

        funcoesUteis.updateFilesRead(self._wayTempFilesRead, file.replace('.txt', '.pdf'), 'ProofsPaymentsItau')
        
        valuesOfLine = {}
        valuesOfFile = []

        dataFile = leTxt(file, treatAsText=True, removeBlankLines=True)

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

        for data in dataFile:

            data = str(data)
            dataSplit = data.split(':')

            fieldOne = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 1))

            fieldTwo = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 2))

            if fieldOne.count('COMPROVANTE DE OPERACAO') > 0:
                category = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(data.split('-'), 2))

            if fieldOne.count('CONTA A SER DEBITADA') > 0:
                self._accountDebitOrCredit = 'DEBIT'
            elif fieldOne.count('CONTA A SER CREDITADA') > 0 or fieldOne.count('DADOS DO PAGAMENTO') > 0:
                self._accountDebitOrCredit = 'CREDIT'

            if self._accountDebitOrCredit == 'DEBIT':
                if fieldOne.count('AGENCIA') > 0:
                    account = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 3))
                    account = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(account.split('-'), 1))
            elif self._accountDebitOrCredit == 'CREDIT':
                if fieldOne == "NOME":
                    nameProvider = fieldTwo

                if fieldOne == "NOME DO FAVORECIDO":
                    nameProvider = fieldTwo
                    namePayee = nameProvider
                
                if fieldOne.count("GUIA DE RECOLHIMENTO") > 0:
                    historic = funcoesUteis.treatTextField(data)
                    
                if fieldOne == "INFORMACOES FORNECIDAS PELO PAGADOR":
                    historic = fieldTwo
                
                if fieldOne == "DATA DE VENCIMENTO":
                    dueDate = funcoesUteis.transformaCampoDataParaFormatoBrasileiro(funcoesUteis.retornaCampoComoData(fieldTwo))

                if ( fieldOne.count("CPF") > 0 or fieldOne.count("CNPJ") > 0 ) and fieldOne.count("PAGADOR") > 0:
                    cgcePaying = str(funcoesUteis.treatNumberField(fieldTwo))

                if ( fieldOne.count("CPF") > 0 or fieldOne.count("CNPJ") > 0 ) and fieldOne.count("PAGADOR") == 0:
                    cnpjProvider = fieldTwo

                if fieldOne.count("VALOR") > 0:
                    amountPaid = funcoesUteis.treatDecimalField(fieldTwo)

			# quando é pagamento de imposto não tem o nome do fornecedor, o dados vem na informação complementar
            if historic != "" and dueDate == "" and namePayee == "":
                nameProvider = historic

            # se o nome do fornecedor ainda for vazio, então considero a categoria como fornecedor
            if nameProvider == "" and category != "":
                nameProvider = category

            for valueOfLinePayment in self._valuesOfLinePayments:
                if data[0 : len(valueOfLinePayment) ] == valueOfLinePayment:
                    paymentDate = funcoesUteis.treatTextField(data[len(valueOfLinePayment)+1:len(valueOfLinePayment)+11])
                    paymentDate = funcoesUteis.retornaCampoComoData(paymentDate.replace('.', '/'))

                    if paymentDate is not None and amountPaid > 0:
                        valuesOfLine = {
                            "paymentDate": paymentDate,
                            "nameProvider": nameProvider,
                            "cnpjProvider": cnpjProvider,
                            "dueDate": dueDate,
                            "bank": bank,
                            "account": account,
                            "amountPaid": amountPaid,
                            "amountDiscount": float(0),
                            "amountInterest": float(0),
                            "amountOriginal": float(0),
                            "historic": historic,
                            "category": category,
                            "cgcePaying": cgcePaying,
                            "foundProof": True
                        }

                        valuesOfFile.append(valuesOfLine.copy())
                    
                    nameProvider = ""
                    namePayee = ""
                    historic = ""
                    dueDate = None
                    cgcePaying = ""
                    cnpjProvider = ""
                    amountPaid = float(0)

                    break

        return valuesOfFile

    def processAll(self):
        for root, dirs, files in os.walk(self._wayTemp):
            for file in files:
                if file.lower().endswith(('.txt')):
                    wayFile = os.path.join(root, file)
                    self._proofs.append(self.process(wayFile))

        return funcoesUteis.removeAnArrayFromWithinAnother(self._proofs)

class SispagItauExcel(object):

    def __init__(self, wayOriginal):
        self._wayOriginal = wayOriginal
        self._proofs = []

    def isProof(self, file):
        dataFile = leXls_Xlsx(file)

        for data in dataFile:
            fieldOne = funcoesUteis.treatTextFieldInVector(data, 1)
            fieldTwo = funcoesUteis.treatTextFieldInVector(data, 2)
            fieldThree = funcoesUteis.treatTextFieldInVector(data, 3)

            if fieldOne == "NOME DO FAVORECIDO" and fieldTwo == "CPF/CNPJ" and fieldThree == "TIPO DE PAGAMENTO":
                return True

    def process(self, file):
        # se não for desta classe nem segue pra frente
        if self.isProof(file) is None:
            return []

        dataFile = leXls_Xlsx(file)

        valuesOfLine = {}
        valuesOfFile = []
        posionsOfHeader = {}

        bank = ""
        for data in dataFile:
            try:
                fieldOne = funcoesUteis.treatTextFieldInVector(data, 1)

                if fieldOne.count('NOME DO FAVORECIDO') > 0:
                    posionsOfHeader.clear()
                    for keyField, nameField in enumerate(data):
                        nameField = funcoesUteis.treatTextField(nameField)
                        posionsOfHeader[nameField] = keyField

                if fieldOne == "AGENCIA/CONTA:":
                    agencyAndAccount = funcoesUteis.treatTextFieldInVector(data, 2)
                    bankSplit = agencyAndAccount.split('/')
                    try:
                        account = funcoesUteis.treatNumberField(bankSplit[1][:-1]) # o -1 é pq o último digíto é o verificador, e nem sempre no extrato tem ele
                    except Exception:
                        account = ""
                    
                    bank = "ITAU" 

                paymentDate = funcoesUteis.treatDateFieldInVector(data, fieldsHeader=posionsOfHeader, nameFieldHeader="Data de pagamento")

                nameProvider = funcoesUteis.treatTextFieldInVector(data, fieldsHeader=posionsOfHeader, nameFieldHeader="Nome do favorecido")

                amountPaid = funcoesUteis.treatDecimalFieldInVector(data, fieldsHeader=posionsOfHeader, nameFieldHeader="Valor do Pagamento (R$)")

                cnpjProvider = funcoesUteis.treatNumberFieldInVector(data, fieldsHeader=posionsOfHeader, nameFieldHeader="CPF/CNPJ")

                if paymentDate is not None and amountPaid > 0:
                    valuesOfLine = {
                        "paymentDate": paymentDate,
                        "nameProvider": nameProvider,
                        "cnpjProvider": cnpjProvider,
                        "amountPaid": amountPaid,
                        "bank": bank,
                        "account": account,
                        "foundProof": True
                    }

                    valuesOfFile.append(valuesOfLine.copy())

            except Exception as e:
                print(e)

        return valuesOfFile

    def processAll(self):
        for root, dirs, files in os.walk(self._wayOriginal):
            for file in files:
                if file.lower().endswith(('.xls', '.xlsx')):
                    wayFile = os.path.join(root, file)
                    self._proofs.append(self.process(wayFile))

        return funcoesUteis.removeAnArrayFromWithinAnother(self._proofs)

# if __name__ == "__main__":
#     proofsPaymentsItau = ProofsPaymentsItau("C:/programming/baymax/backend/accounting_integration/data/temp/890")
#     print(len(proofsPaymentsItau.processAll()))

    # sispagItauExcel = SispagItauExcel("C:/integracao_contabil/1428/arquivos_originais/Sispag detalhada.xlsx")
    # print(sispagItauExcel.process())
            