import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import json
from tools.leArquivos import leXls_Xlsx, leTxt
import tools.funcoesUteis as funcoesUteis


# este 'por moeda' é a forma que o cliente gera o relatório no sistema da Lys
class PaymentsLysPorMoeda(object):
    def __init__(self, wayOriginalToRead):
        self._payments = []
        self._wayOriginalToRead = wayOriginalToRead

    def isPaymentsLysPorMoeda(self, file):
        dataFile = leXls_Xlsx(file)

        for data in dataFile:
            identificationField = funcoesUteis.treatTextFieldInVector(data, 5)
            if identificationField.count('NMPESSOACREDORA') > 0:
                return True

    def process(self, file):

        if self.isPaymentsLysPorMoeda(file) is not True:
            return []

        valuesOfLine = {}
        valuesOfFile = []
        posionsOfHeader = {}

        dataFile = leXls_Xlsx(file)

        for data in dataFile:
            try:
                headerField = funcoesUteis.treatTextFieldInVector(data, 5)
                if headerField.count('NMPESSOACREDORA') > 0:
                    posionsOfHeader.clear()
                    for keyField, nameField in enumerate(data):
                        nameField = funcoesUteis.treatTextField(nameField)
                        posionsOfHeader[nameField] = keyField
                    continue

                idAccountPaid = funcoesUteis.treatTextFieldInVector(data, 1, posionsOfHeader, "idsContaPagar")
                paymentDate = funcoesUteis.treatDateFieldInVector(data, 14, posionsOfHeader, "dtPagamento")
                accountCode = funcoesUteis.treatNumberFieldInVector(data, 23, posionsOfHeader, "nrContaContabil")

                bankAndAccount = funcoesUteis.treatTextFieldInVector(data, 20, posionsOfHeader, "idFonte")

                positionWordBank = bankAndAccount.find('BANCO')
                if positionWordBank >= 0:
                    positionPlusSign = bankAndAccount[positionWordBank:].find('>') + positionWordBank
                    bank = funcoesUteis.returnBankForName(funcoesUteis.treatTextField(bankAndAccount[ positionWordBank+6 : positionPlusSign ]))

                    positionWordAccount = bankAndAccount.find('CONTA')
                    positionSplitSign = bankAndAccount[positionWordAccount:].find('/') + positionWordAccount + 1
                    accountBank = funcoesUteis.treatTextField(bankAndAccount[ positionSplitSign: ])
                else:
                    bank = "DINHEIRO"
                    accountBank = ""

                if paymentDate is not None:
                    valuesOfLine = {
                        "idAccountPaid": idAccountPaid,
                        "paymentDate": funcoesUteis.transformaCampoDataParaFormatoBrasileiro(paymentDate),
                        "bank": bank,
                        "accountBank": accountBank,
                        "accountCode": accountCode
                    }

                    valuesOfFile.append(valuesOfLine.copy())
            except Exception:
                pass
        return valuesOfFile

    def processAll(self):
        for root, dirs, files in os.walk(self._wayOriginalToRead):
            for file in files:
                wayFile = os.path.join(root, file)

                if file.lower().endswith(('.xls', '.xlsx')):
                    self._payments.append(self.process(wayFile))

        return funcoesUteis.removeAnArrayFromWithinAnother(self._payments)


# este 'por data' é a forma que o cliente gera o relatório no sistema da Lys
class PaymentsLysPorData(object):
    def __init__(self, wayOriginalToRead, paymentsPorMoeda=[]):
        self._paymentsPorMoeda = paymentsPorMoeda
        self._payments = []
        self._wayOriginalToRead = wayOriginalToRead

    def isPaymentsLysPorData(self, file):
        dataFile = leXls_Xlsx(file)

        for data in dataFile:
            identificationField = funcoesUteis.treatTextFieldInVector(data, 5)
            if identificationField.count('IDPESSOACREDORA') > 0:
                return True

    def returnDataPaymentsPorMoeda(self, idAccountPaid):
        for paymentMoeda in self._paymentsPorMoeda:
            if paymentMoeda["idAccountPaid"] == idAccountPaid:
                return paymentMoeda

    def process(self, file):

        if self.isPaymentsLysPorData(file) is not True:
            return []
            
        dataFile = leXls_Xlsx(file)

        valuesOfLine = {}
        valuesOfFile = []
        posionsOfHeader = {}

        for data in dataFile:
            try:
                headerField = funcoesUteis.treatTextFieldInVector(data, 5)
                if headerField.count('IDPESSOACREDORA') > 0:
                    posionsOfHeader.clear()
                    for keyField, nameField in enumerate(data):
                        nameField = funcoesUteis.treatTextField(nameField)
                        posionsOfHeader[nameField] = keyField
                    continue

                idAccountPaid = funcoesUteis.treatTextFieldInVector(data, 1, posionsOfHeader, "idsContaPagar")
                parcelNumber = funcoesUteis.treatTextFieldInVector(data, 2, posionsOfHeader, "cdParcela")
                dueDate = funcoesUteis.transformaCampoDataParaFormatoBrasileiro(funcoesUteis.treatDateFieldInVector(data, 4, posionsOfHeader, "dtVencimento"))
                nameProvider = funcoesUteis.treatTextFieldInVector(data, 6, posionsOfHeader, "nmPessoaCredora")
                document = funcoesUteis.treatTextFieldInVector(data, 11, posionsOfHeader, "nrDocFiscalOriginal")
                issueDate = funcoesUteis.transformaCampoDataParaFormatoBrasileiro(funcoesUteis.treatDateFieldInVector(data, 12, posionsOfHeader, "dtEmissao"))
                amountPaid = funcoesUteis.treatDecimalFieldInVector(data, 36, posionsOfHeader, "valorLiquido")
                amountDiscount = funcoesUteis.treatDecimalFieldInVector(data, 19, posionsOfHeader, "valordesconto")
                amountInterest = funcoesUteis.treatDecimalFieldInVector(data, 20, posionsOfHeader, "valormulta")
                amountFine = funcoesUteis.treatDecimalFieldInVector(data, 30, posionsOfHeader, "valorjuro")
                amountOriginal = funcoesUteis.treatDecimalFieldInVector(data, 10)
                historic = funcoesUteis.treatTextFieldInVector(data, 34, posionsOfHeader, "justificaticaDaConta")

                paymentsMoeda = self.returnDataPaymentsPorMoeda(idAccountPaid)

                paymentDate = funcoesUteis.analyzeIfFieldIsValid(paymentsMoeda, "paymentDate", None)
                bank = funcoesUteis.analyzeIfFieldIsValid(paymentsMoeda, "bank")
                accountBank = funcoesUteis.analyzeIfFieldIsValid(paymentsMoeda, "accountBank")
                accountCode = funcoesUteis.analyzeIfFieldIsValid(paymentsMoeda, "accountCode")
                
                if paymentDate is not None and amountPaid > 0:
                    valuesOfLine = {
                        "document": document,
                        "parcelNumber": parcelNumber,
                        "nameProvider": nameProvider,
                        "paymentDate": paymentDate,
                        "dueDate": dueDate,
                        "issueDate": issueDate,
                        "bank": bank,
                        "account": accountBank,
                        "amountPaid": amountPaid,
                        "amountDiscount": amountDiscount,
                        "amountInterest": amountInterest,
                        "amountFine": amountFine,
                        "amountOriginal": amountOriginal,
                        "accountCodeOld": accountCode,
                        "historic": historic
                    }

                    valuesOfFile.append(valuesOfLine.copy())
            except Exception:
                pass
        return valuesOfFile

    def processAll(self):
        for root, dirs, files in os.walk(self._wayOriginalToRead):
            for file in files:
                wayFile = os.path.join(root, file)

                if file.lower().endswith(('.xls', '.xlsx')):
                    self._payments.append(self.process(wayFile))

        return funcoesUteis.removeAnArrayFromWithinAnother(self._payments)

# if __name__ == "__main__":
#     paymentsLysPorMoeda = PaymentsLysPorMoeda("C:/integracao_contabil/1777/arquivos_originais/LD POR MOEDA.XLS")
#     paymentsMoeda = paymentsLysPorMoeda.process()

#     paymentsLysPorData = PaymentsLysPorData("C:/integracao_contabil/1777/arquivos_originais/LD POR DATA.XLS", paymentsMoeda)
#     print(paymentsLysPorData.process())
