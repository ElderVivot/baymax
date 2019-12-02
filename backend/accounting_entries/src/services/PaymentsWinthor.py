import sys
import os

fileDir = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(os.path.join(fileDir, 'backend'))

from tools.leArquivos import leXls_Xlsx, leTxt
import tools.funcoesUteis as funcoesUteis


class PaymentsWinthorPDF(object):
    def __init__(self):
        self._valuesPaymentDates = {}
        self._paymentDate = None
        self._valuesOfLine = []

    def returnPaymentsDates(self, file):
        dataFile = leTxt(file)

        # primeiro percorre e divide cada campo separando por um espaço
        for data in dataFile:

            data = str(data).strip()
            data = funcoesUteis.handlesTextField(data)

            fieldsSeparatedBySpace = data.split(' ')

            self._valuesOfLine.append(fieldsSeparatedBySpace)

        # percorre os campos ajustados e faz o tratamento
        for key, valueOfLine in enumerate(self._valuesOfLine):
            try:
                if valueOfLine[0] == "DT.PAGAMENTO:":
                    self._paymentDate = funcoesUteis.transformaCampoDataParaFormatoBrasileiro(\
                        funcoesUteis.retornaCampoComoData(valueOfLine[1]))

                if funcoesUteis.handlesNumberField(valueOfLine[0]).isnumeric() and self._valuesOfLine[key+1][0] == "HISTORICO":
                    self._valuesPaymentDates[valueOfLine[0]] = self._paymentDate
            except Exception as e:
                print(e)
        
        return self._valuesPaymentDates


class PaymentsWinthorExcel(object):

    def __init__(self):
        self._valuesOfLine = {}
        self._valuesOfFile = []
    
    def processPayments(self, file, paymentDatesByIdLanc):
        dataFile = leXls_Xlsx(file)

        for data in dataFile:

            try:
                idLanc = funcoesUteis.handlesNumberFieldInVector(data, 0)

                paymentDate = paymentDatesByIdLanc[idLanc]
                print(paymentDate)

                # self._valuesOfLine = {
                #     "paymentDate": funcoesUteis.handlesTextFieldInVector(data[])
                # }
            except Exception as e:
                print(e)


if __name__ == "__main__":
    paymentsWinthorPDF = PaymentsWinthorPDF()
    paymentDates = paymentsWinthorPDF.returnPaymentsDates("C:\\Programming\\tests\\transform_pdf\\teste.txt")

    paymentsWinthorExcel = PaymentsWinthorExcel()
    paymentsWinthorExcel.processPayments("E:\\soma\\integracao\\Diviart\\Contas Pagas.xls", paymentDates)

