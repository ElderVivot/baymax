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
    def __init__(self, file):
        self._valuesOfLine = {}
        self._valuesOfFile = []
        self._posionsOfHeader = {}
        self._file = file

    def isPaymentsLysPorMoeda(self):
        dataFile = leXls_Xlsx(self._file)

        for data in dataFile:
            try:
                if str(data[4]).upper().count('NMPESSOACREDORA') > 0:
                    return True
            except Exception:
                pass

    def process(self):

        if self.isPaymentsLysPorMoeda() is True:
            dataFile = leXls_Xlsx(self._file)

            for data in dataFile:
                try:
                    if str(data[4]).upper().count('NMPESSOACREDORA') > 0:
                        self._posionsOfHeader.clear()
                        for keyField, nameField in enumerate(data):
                            nameField = funcoesUteis.treatTextField(nameField)
                            self._posionsOfHeader[nameField] = keyField
                        continue

                    idAccountPaid = funcoesUteis.treatTextFieldInVector(data, 1, self._posionsOfHeader, "idsContaPagar")
                    paymentDate = funcoesUteis.treatDateFieldInVector(data, 14, self._posionsOfHeader, "dtPagamento")
                    accountCode = funcoesUteis.treatNumberFieldInVector(data, 23, self._posionsOfHeader, "nrContaContabil")

                    bankAndAccount = funcoesUteis.treatTextFieldInVector(data, 20, self._posionsOfHeader, "idFonte")

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
                        self._valuesOfLine = {
                            "idAccountPaid": idAccountPaid,
                            "paymentDate": funcoesUteis.transformaCampoDataParaFormatoBrasileiro(paymentDate),
                            "bank": bank,
                            "accountBank": accountBank,
                            "accountCode": accountCode
                        }

                        self._valuesOfFile.append(self._valuesOfLine.copy())
                except Exception:
                    pass
            return self._valuesOfFile


# este 'por data' é a forma que o cliente gera o relatório no sistema da Lys
class PaymentsLysPorData(object):
    def __init__(self, file, paymentsPorMoeda=[]):
        self._valuesOfLine = {}
        self._valuesOfFile = []
        self._posionsOfHeader = {}
        self._file = file
        self._paymentsPorMoeda = paymentsPorMoeda

    def isPaymentsLysPorData(self):
        dataFile = leXls_Xlsx(self._file)

        for data in dataFile:
            try:
                if str(data[4]).upper().count('IDPESSOACREDORA') > 0:
                    return True
            except Exception:
                pass

    def returnDataPaymentsPorMoeda(self, idAccountPaid):
        for paymentMoeda in self._paymentsPorMoeda:
            if paymentMoeda["idAccountPaid"] == idAccountPaid:
                return paymentMoeda

    def process(self):

        if self.isPaymentsLysPorData() is True:
            dataFile = leXls_Xlsx(self._file)

            for data in dataFile:
                try:
                    if str(data[4]).upper().count('IDPESSOACREDORA') > 0:
                        self._posionsOfHeader.clear()
                        for keyField, nameField in enumerate(data):
                            nameField = funcoesUteis.treatTextField(nameField)
                            self._posionsOfHeader[nameField] = keyField
                        continue

                    idAccountPaid = funcoesUteis.treatTextFieldInVector(data, 1, self._posionsOfHeader, "idsContaPagar")
                    parcelNumber = funcoesUteis.treatTextFieldInVector(data, 2, self._posionsOfHeader, "cdParcela")
                    dueDate = funcoesUteis.transformaCampoDataParaFormatoBrasileiro(funcoesUteis.treatDateFieldInVector(data, 4, self._posionsOfHeader, "dtVencimento"))
                    nameProvider = funcoesUteis.treatTextFieldInVector(data, 6, self._posionsOfHeader, "nmPessoaCredora")
                    document = funcoesUteis.treatTextFieldInVector(data, 11, self._posionsOfHeader, "nrDocFiscalOriginal")
                    issueDate = funcoesUteis.transformaCampoDataParaFormatoBrasileiro(funcoesUteis.treatDateFieldInVector(data, 12, self._posionsOfHeader, "dtEmissao"))
                    amountPaid = funcoesUteis.treatDecimalFieldInVector(data, 36)
                    amountDiscount = funcoesUteis.treatDecimalFieldInVector(data, 19, self._posionsOfHeader, "valordesconto")
                    amountInterest = funcoesUteis.treatDecimalFieldInVector(data, 20, self._posionsOfHeader, "valormulta")
                    amountFine = funcoesUteis.treatDecimalFieldInVector(data, 30, self._posionsOfHeader, "valorjuro")
                    amountOriginal = funcoesUteis.treatDecimalFieldInVector(data, 10)
                    historic = funcoesUteis.treatTextFieldInVector(data, 34, self._posionsOfHeader, "justificaticaDaConta")

                    paymentsMoeda = self.returnDataPaymentsPorMoeda(idAccountPaid)

                    paymentDate = funcoesUteis.analyzeIfFieldIsValid(paymentsMoeda, "paymentDate", None)
                    bank = funcoesUteis.analyzeIfFieldIsValid(paymentsMoeda, "bank")
                    accountBank = funcoesUteis.analyzeIfFieldIsValid(paymentsMoeda, "accountBank")
                    accountCode = funcoesUteis.analyzeIfFieldIsValid(paymentsMoeda, "accountCode")
                    
                    if paymentDate is not None:
                        self._valuesOfLine = {
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

                        self._valuesOfFile.append(self._valuesOfLine.copy())
                except Exception:
                    pass
            return self._valuesOfFile

# if __name__ == "__main__":
#     paymentsLysPorMoeda = PaymentsLysPorMoeda("C:/integracao_contabil/1777/arquivos_originais/LD POR MOEDA.XLS")
#     paymentsMoeda = paymentsLysPorMoeda.process()

#     paymentsLysPorData = PaymentsLysPorData("C:/integracao_contabil/1777/arquivos_originais/LD POR DATA.XLS", paymentsMoeda)
#     print(paymentsLysPorData.process())
