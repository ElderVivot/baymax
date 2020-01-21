import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import json
from tools.leArquivos import leXls_Xlsx, leTxt, readJson
import tools.funcoesUteis as funcoesUteis


class PaymentsSerraThermas(object):

    def __init__(self, codiEmp, wayOriginalToRead, wayTemp, settings):
        self._codiEmp = codiEmp
        self._wayOriginalToRead = wayOriginalToRead
        self._wayTemp = wayTemp
        self._payments = []
        # self._wayTempFilesRead = os.path.join(wayTemp, 'FilesReads.json')
        self._settings = settings

    def isPayment(self, file):
        dataFile = leXls_Xlsx(file)

        for data in dataFile:
            textOne = funcoesUteis.treatTextFieldInVector(data, 1)

            textTwo = funcoesUteis.treatTextFieldInVector(data, 2)

            if textOne == "DATA" and textTwo == "CREDITO":
                return True

    def process(self, file):
        # se não for desta classe nem segue pra frente
        # funcoesUteis.updateFilesRead(self._wayTempFilesRead, file.replace('.txt', '.pdf'), 'PaymentsWinthorExcel')
        if self.isPayment is None:
            return []

        dataFile = leXls_Xlsx(file)

        valuesOfLine = {}
        valuesOfFile = []
        posionsOfHeader = {}

        paymentDate = None

        for key, data in enumerate(dataFile):

            try:
                textOne = funcoesUteis.treatTextFieldInVector(data, 1)
                textTwo = funcoesUteis.treatTextFieldInVector(data, 2)

                if textOne.count('DATA') > 0 and textTwo == "CREDITO":
                    posionsOfHeader.clear()
                    for keyField, nameField in enumerate(data):
                        nameField = funcoesUteis.treatTextField(nameField)
                        posionsOfHeader[nameField] = keyField
                    continue

                paymentDateTemp = funcoesUteis.retornaCampoComoData(funcoesUteis.treatTextFieldInVector(data, 1, posionsOfHeader, "Data"))
                if paymentDateTemp is not None:
                    paymentDate = paymentDateTemp

                nameProvider = funcoesUteis.treatTextFieldInVector(data, 4, posionsOfHeader, "Descricao")
                cgceProvider = funcoesUteis.treatTextFieldInVector(data, 6, posionsOfHeader, "CNPJ")
                document = ""
                historic = funcoesUteis.treatTextFieldInVector(data, 5, posionsOfHeader, "OBS")
                amountPaid = funcoesUteis.treatDecimalFieldInVector(data, 3, posionsOfHeader, "DEBITO")
                bank = "BRADESCO" # a planilha é preenchida pelo cliente, e tem apenas um banco
                account = "49000" # a planilha é preenchida pelo cliente, e tem apenas uma conta

                if amountPaid > 0:
                    valuesOfLine = {
                        "paymentDate": funcoesUteis.transformaCampoDataParaFormatoBrasileiro(paymentDate),
                        "nameProvider": nameProvider,
                        "cgceProvider": cgceProvider,
                        "document": document,
                        "bank": bank,
                        "account": account,
                        "amountPaid": amountPaid,
                        "historic": historic
                    }

                    valuesOfFile.append(valuesOfLine.copy())

            except Exception as e:
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
#     paymentsWinthorPDF = PaymentsWinthorPDF("C:/_temp/integracao_diviart/teste.txt")
#     paymentDates = paymentsWinthorPDF.returnPaymentsDates()

#     paymentsWinthorExcel = PaymentsWinthorExcel("1428")
#     print(paymentsWinthorExcel.processPayments("C:/_temp/integracao_diviart/Contas Pagas.xls", paymentDates))

