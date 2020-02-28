import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import tools.funcoesUteis as funcoesUteis
from tools.leArquivos import leXls_Xlsx


class ReadExcelToUpdateOrExportData(object):

    def __init__(self, file):
        self._file = file
        self._paymentsOfLine = {}
        self._paymentsOfFile = []
        self._posionsOfHeaderPayments = {}
        self._extractsOfLine = {}
        self._extractsOfFile = []
        self._posionsOfHeaderExtracts = {}

    def getPayments(self):
        dataFile = leXls_Xlsx(self._file, 'Pagamentos')

        for data in dataFile:
            if str(data[0]).upper().count('DOCUMENTO') > 0:
                self._posionsOfHeaderPayments.clear()
                for keyField, nameField in enumerate(data):
                    nameField = funcoesUteis.treatTextField(nameField)
                    self._posionsOfHeaderPayments[nameField] = keyField
                continue

            numberLote = funcoesUteis.treatNumberFieldInVector(data, 1, self._posionsOfHeaderPayments, "Lote")
            document = funcoesUteis.treatTextFieldInVector(data, 2, self._posionsOfHeaderPayments, "Documento")

            findNote = funcoesUteis.treatTextFieldInVector(data, 3, self._posionsOfHeaderPayments, "NF na Domínio?")
            if findNote == "1":
                findNote = True
            elif findNote == "0":
                findNote = False
            else:
                findNote = ""

            parcelNumber = funcoesUteis.treatTextFieldInVector(data, 4, self._posionsOfHeaderPayments, "Parcela")
            nameProvider = funcoesUteis.treatTextFieldInVector(data, 5, self._posionsOfHeaderPayments, "Fornecedor")
            cgceProvider = funcoesUteis.treatTextFieldInVector(data, 6, self._posionsOfHeaderPayments, "CNPJ Fornecedor")

            bankAndAccount = funcoesUteis.treatTextFieldInVector(data, 7, self._posionsOfHeaderPayments, "Banco Financeiro").split('-')
            if len(bankAndAccount) == 2:
                bank = bankAndAccount[0]
                account = bankAndAccount[1]
            elif len(bankAndAccount) == 1:
                bank = bankAndAccount[0]
                account = ""
            else:
                bank = ""
                account = ""
                
            bankAndAccountExtract = funcoesUteis.treatTextFieldInVector(data, 8, self._posionsOfHeaderPayments, "Banco Extrato").split('-')
            if len(bankAndAccountExtract) == 2:
                bankExtract = bankAndAccountExtract[0]
                accountExtract = bankAndAccountExtract[1]
            elif len(bankAndAccountExtract) == 1:
                bankExtract = bankAndAccountExtract[0]
                accountExtract = ""
            else:
                bankExtract = ""
                accountExtract = ""

            foundProof = funcoesUteis.treatTextFieldInVector(data, 9, self._posionsOfHeaderPayments, "Comprovante Pagto?")
            if foundProof == "1":
                foundProof = True
            elif foundProof == "0":
                foundProof = False
            else:
                foundProof = ""

            paymentDate = funcoesUteis.treatDateFieldInVector(data, 10, self._posionsOfHeaderPayments, "Data Financeiro")
            extractDate = funcoesUteis.treatDateFieldInVector(data, 11, self._posionsOfHeaderPayments, "Data Extrato")
            dateOfImport = funcoesUteis.treatDateFieldInVector(data, 12, self._posionsOfHeaderPayments, "Importação Domínio")
            dueDate = funcoesUteis.treatTextFieldInVector(data, 13, self._posionsOfHeaderPayments, "Vencimento")
            issueDate = funcoesUteis.treatTextFieldInVector(data, 14, self._posionsOfHeaderPayments, "Emissão")
            amountPaid = funcoesUteis.treatDecimalFieldInVector(data, 15, self._posionsOfHeaderPayments, "Valor Pago")
            amountDiscount = funcoesUteis.treatDecimalFieldInVector(data, 16, self._posionsOfHeaderPayments, "Desconto")
            amountInterest = funcoesUteis.treatDecimalFieldInVector(data, 17, self._posionsOfHeaderPayments, "Juros")
            amountFine = funcoesUteis.treatDecimalFieldInVector(data, 18, self._posionsOfHeaderPayments, "Multa")
            amountOriginal = funcoesUteis.treatDecimalFieldInVector(data, 19, self._posionsOfHeaderPayments, "Valor Original")
            accountCode = funcoesUteis.treatNumberFieldInVector(data, 20, self._posionsOfHeaderPayments, "Conta Contabil Domínio")
            codiEmp = funcoesUteis.treatTextFieldInVector(data, 21, self._posionsOfHeaderPayments, "Codigo Empresa")
            historic = funcoesUteis.treatTextFieldInVector(data, 22, self._posionsOfHeaderPayments, "Historico Planilha")
            category = funcoesUteis.treatTextFieldInVector(data, 23, self._posionsOfHeaderPayments, "Categoria")
            accountPlan = funcoesUteis.treatTextFieldInVector(data, 24, self._posionsOfHeaderPayments, "Plano de Contas")
            cgcePaying = funcoesUteis.treatTextFieldInVector(data, 25, self._posionsOfHeaderPayments, "CNPJ Pagador")
            historicExtract = funcoesUteis.treatTextFieldInVector(data, 26, self._posionsOfHeaderPayments, "Historico Extrato Bancário")
            accountCodeOld = funcoesUteis.treatTextFieldInVector(data, 27, self._posionsOfHeaderPayments, "Conta Contabil Sistema Cliente")

            if amountPaid != 0:
                self._paymentsOfLine = {
                    "numberLote": numberLote,
                    "document": document,
                    "findNote": findNote,
                    "parcelNumber": parcelNumber,
                    "nameProvider": nameProvider,
                    "cgceProvider": cgceProvider,
                    "bank": bank,
                    "account": account,
                    "bankExtract": bankExtract,
                    "accountExtract": accountExtract,
                    "foundProof": foundProof,
                    "paymentDate": paymentDate,
                    "dateExtract": extractDate,
                    "dateOfImport": dateOfImport,
                    "dueDate": dueDate,
                    "issueDate": issueDate,
                    "amountPaid": amountPaid,
                    "amountDiscount": amountDiscount,
                    "amountInterest": amountInterest,
                    "amountFine": amountFine,
                    "amountOriginal": amountOriginal,
                    "accountCode": accountCode,
                    "codiEmp": codiEmp,
                    "historic": historic,
                    "category": category,
                    "accountPlan": accountPlan,
                    "cgcePaying": cgcePaying,
                    "historicExtract": historicExtract,
                    "accountCodeOld": accountCodeOld
                }

                self._paymentsOfFile.append(self._paymentsOfLine.copy())

        return self._paymentsOfFile

    def getExtracts(self):
        dataFile = leXls_Xlsx(self._file, 'ExtratosBancarios')

        for key, data in enumerate(dataFile):
            if str(data[0]).upper().count('DATA') > 0:
                self._posionsOfHeaderExtracts.clear()
                for keyField, nameField in enumerate(data):
                    nameField = funcoesUteis.treatTextField(nameField)
                    self._posionsOfHeaderExtracts[nameField] = keyField
                continue

            dateExtract = funcoesUteis.treatDateFieldInVector(data, 1, self._posionsOfHeaderExtracts, "Data")
            accountCodeDebit = funcoesUteis.treatNumberFieldInVector(data, 2, self._posionsOfHeaderExtracts, "Debito")
            accountCodeCredit = funcoesUteis.treatNumberFieldInVector(data, 3, self._posionsOfHeaderExtracts, "Credito")
            amount = funcoesUteis.treatDecimalFieldInVector(data, 4, self._posionsOfHeaderExtracts, "Valor")
            historicCode = funcoesUteis.treatNumberFieldInVector(data, 5, self._posionsOfHeaderExtracts, "Cod. Hist")
            historic = funcoesUteis.treatTextFieldInVector(data, 6, self._posionsOfHeaderExtracts, "Historico")

            foundProofInPayments = funcoesUteis.treatTextFieldInVector(data, 7, self._posionsOfHeaderExtracts, "Encontrou no Financeiro?")
            if foundProofInPayments == "1":
                foundProofInPayments = True
            elif foundProofInPayments == "0":
                foundProofInPayments = False
            else:
                foundProofInPayments = ""

            bank = funcoesUteis.treatTextFieldInVector(data, 10, self._posionsOfHeaderExtracts, "Banco")
            account = funcoesUteis.treatTextFieldInVector(data, 11, self._posionsOfHeaderExtracts, "Conta Corrente")
            typeTransaction = funcoesUteis.treatTextFieldInVector(data, 13, self._posionsOfHeaderExtracts, "Tipo Transacao")
            operation = funcoesUteis.treatTextFieldInVector(data, 14, self._posionsOfHeaderExtracts, "Operacao")
            document = funcoesUteis.treatTextFieldInVector(data, 16, self._posionsOfHeaderExtracts, "Documento")

            self._extractsOfLine = {
                "dateTransaction": dateExtract,
                "accountCodeDebit": accountCodeDebit,
                "accountCodeCredit": accountCodeCredit,
                "amount": amount,
                "historicCode": historicCode,
                "historic": historic,
                "foundProofInPayments": foundProofInPayments,
                "bank": bank,
                "account": account,
                "typeTransaction": typeTransaction,
                "operation": operation,
                "document": document
            }

            self._extractsOfFile.append(self._extractsOfLine.copy())

        return self._extractsOfFile