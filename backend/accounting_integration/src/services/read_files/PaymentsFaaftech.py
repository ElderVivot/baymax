import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import json
from tools.leArquivos import leXls_Xlsx, leTxt, readJson
import tools.funcoesUteis as funcoesUteis


class PaymentsFaaftech(object):

    def __init__(self, codiEmp, wayOriginalToRead, settings):
        self._codiEmp = codiEmp
        self._wayOriginalToRead = wayOriginalToRead
        self._payments = []
        self._wayTempFilesRead = os.path.join(wayTemp, 'FilesReads.json')
        self._settings = settings

    # def isPayment(self, file):
    #     dataFile = leXls_Xlsx(file)

    #     for data in dataFile:
    #         textComparateOne = funcoesUteis.treatTextFieldInVector(data, 2)

    #         textCompara = funcoesUteis.treatTextFieldInVector(data, 8)

    #         if textHistoric == "HISTORICO" and ( textUser == "USU.LANC." or textUser == "USU. LANC." ):
    #             return True
        
    def process(self, file):
        # se não for desta classe nem segue pra frente
        # funcoesUteis.updateFilesRead(self._wayTempFilesRead, file.replace('.txt', '.pdf'), 'PaymentsWinthorExcel')

        dataFile = leXls_Xlsx(file)

        valuesOfLine = {}
        valuesOfFile = []
        posionsOfHeader = {}

        for key, data in enumerate(dataFile):

            try:
                if str(data[4]).upper().count('NRO NOTA') > 0:
                        posionsOfHeader.clear()
                        for keyField, nameField in enumerate(data):
                            nameField = funcoesUteis.treatTextField(nameField)
                            posionsOfHeader[nameField] = keyField
                        continue

                paymentDate = funcoesUteis.retornaCampoComoData(funcoesUteis.treatTextFieldInVector(data, 4, posionsOfHeader, "Data Baixa"))
                nameProvider = funcoesUteis.treatTextFieldInVector(data, 4, posionsOfHeader, "Nome Parceiro")
                document = funcoesUteis.treatTextFieldInVector(data, 3, posionsOfHeader, "Nro Nota")
                accountPlan = funcoesUteis.treatTextFieldInVector(data, 7, posionsOfHeader, "Descricao (Natureza)")
                dueDate = funcoesUteis.retornaCampoComoData(funcoesUteis.treatTextFieldInVector(data, 5, posionsOfHeader, "Dt. Vencimento"))
                historic = ""
                parcelNumber = ""
                amountPaid = funcoesUteis.treatDecimalFieldInVector(data, 19, posionsOfHeader, "Vlr Baixa")
                amountDevolution = funcoesUteis.treatDecimalFieldInVector(0.0)
                amountDiscount = funcoesUteis.treatDecimalFieldInVector(data, 41, posionsOfHeader, "Vlr Desconto")
                amountInterest = funcoesUteis.treatDecimalFieldInVector(data, 44, posionsOfHeader, "Vlr Juros")
                amountFine = funcoesUteis.treatDecimalFieldInVector(data, 45, posionsOfHeader, "Vlr Multa")
                amountOriginal = funcoesUteis.treatDecimalFieldInVector(data, 45, posionsOfHeader, "Valor Liquido")
                paymentType = ""

                bank = funcoesUteis.treatTextFieldInVector(data, 24)
                bankVector = self.returnBank(bank)
                bank = funcoesUteis.treatTextFieldInVector(bankVector, 1)

                account = ""

                companyBranch = funcoesUteis.treatTextFieldInVector(data, 28)

                if paymentDate is not None and amountPaid > 0:
                    valuesOfLine = {
                        "paymentDate": funcoesUteis.transformaCampoDataParaFormatoBrasileiro(paymentDate),
                        "nameProvider": nameProvider,
                        "document": document,
                        "parcelNumber": parcelNumber,
                        "bank": bank,
                        "account": account,
                        "amountPaid": amountPaid,
                        "amountDiscount": amountDiscount,
                        "amountInterest": amountInterest,
                        "amountOriginal": amountOriginal,
                        "amountDevolution": amountDevolution,
                        "bankCheck": bankCheck,
                        "paymentType": paymentType,
                        "accountPlan": accountPlan,
                        "historic": historic,
                        "companyBranch": companyBranch
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

