import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

from tools.leArquivos import leXls_Xlsx, leTxt, readJson
import tools.funcoesUteis as funcoesUteis


class LivroCaixaRural(object):

    def __init__(self, codiEmp, wayOriginalToRead):
        self._codiEmp = codiEmp
        self._wayOriginalToRead = wayOriginalToRead
        self._livroCaixaRural = []

    def process(self, file):
        dataFile = leTxt(file)

        valuesOfLine = {}
        valuesOfFile = []

        for key, data in enumerate(dataFile):

            try:
                recordType = data[0:2]
                dateLivro = data[3:11]
                account = data[11:19]
                historic = data[19:274]
                amount = data[274:287]

                if account[0] == "1":
                    amountEntry = amount
                else:
                    amountOutput = amount

                # valuesOfLine = {

                # }            

                valuesOfFile.append(valuesOfLine.copy())

            except Exception as e:
                pass

        return valuesOfFile

    def processAll(self):
        for root, dirs, files in os.walk(self._wayOriginalToRead):
            for file in files:
                wayFile = os.path.join(root, file)

                if file.lower().endswith(('.xls', '.xlsx')):
                    self._livroCaixaRural.append(self.process(wayFile))

        return funcoesUteis.removeAnArrayFromWithinAnother(self._livroCaixaRural)

# if __name__ == "__main__":
#     paymentsWinthorPDF = PaymentsWinthorPDF("C:/_temp/integracao_diviart/teste.txt")
#     paymentDates = paymentsWinthorPDF.returnPaymentsDates()

#     paymentsWinthorExcel = PaymentsWinthorExcel("1428")
#     print(paymentsWinthorExcel.processPayments("C:/_temp/integracao_diviart/Contas Pagas.xls", paymentDates))

