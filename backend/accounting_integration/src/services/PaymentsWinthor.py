import sys
import os

fileDir = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(os.path.join(fileDir, 'backend'))

import json
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
                
                # identifica se é uma linha de lançamento com o idLanc devidamente preenchido
                if funcoesUteis.handlesNumberField(valueOfLine[0]).isnumeric() and ( self._valuesOfLine[key+1][0] == "HISTORICO" \
                     or ( valueOfLine[1].isnumeric() and valueOfLine[2].isnumeric() ) ):
                    self._valuesPaymentDates[valueOfLine[0]] = self._paymentDate
            except Exception as e:
                print(e)
        
        return self._valuesPaymentDates


class PaymentsWinthorExcel(object):

    def __init__(self):
        self._valuesOfLine = {}
        self._valuesOfFile = []
    # backend/accounting_integration/data
    def readValuesOfBank(self, file):
        try:
            readFile = open(file)
            self._valuesOfBanks = json.load(readFile)
            readFile.close()
        except Exception:
            self._valuesOfBanks = {}

    def processPayments(self, file, paymentDatesByIdLanc):
        dataFile = leXls_Xlsx(file)

        for key, data in enumerate(dataFile):

            try:
                idLanc = funcoesUteis.handlesNumberFieldInVector(data, 1)

                paymentDate = paymentDatesByIdLanc[idLanc]
                paymentDate = funcoesUteis.retornaCampoComoData(paymentDate)

                nameProvider = funcoesUteis.handlesTextFieldInVector(data, 9)

                document = funcoesUteis.handlesTextFieldInVector(data, 11)

                accountPlan = funcoesUteis.handlesTextFieldInVector(data, 6)

                historic = funcoesUteis.handlesTextFieldInVector(data, 4)
                if paymentDate is not None and historic == "":
                    historic = funcoesUteis.handlesTextFieldInVector(dataFile[key+1], 4)

                parcelNumber = funcoesUteis.handlesNumberFieldInVector(data, 13)

                amountPaid = funcoesUteis.handlesDecimalFieldInVector(data, 15)

                amountDevolution = funcoesUteis.handlesDecimalFieldInVector(data, 17)

                amountDiscount = funcoesUteis.handlesDecimalFieldInVector(data, 18)

                amountInterest = funcoesUteis.handlesDecimalFieldInVector(data, 19)

                amountOriginal = funcoesUteis.handlesDecimalFieldInVector(data, 21)

                paymentType = funcoesUteis.handlesTextFieldInVector(data, 22)

                bank = funcoesUteis.handlesTextFieldInVector(data, 24)
                try:
                    bank = self._valuesOfBanks[bank]
                except Exception:
                    bank = bank

                bankCheck = funcoesUteis.handlesTextFieldInVector(data, 25)

                companyBranch = funcoesUteis.handlesTextFieldInVector(data, 28)

                if paymentDate is not None and amountPaid > 0:
                    self._valuesOfLine = {
                        "paymentDate": funcoesUteis.transformaCampoDataParaFormatoBrasileiro(paymentDate),
                        "nameProvider": nameProvider,
                        "document": document,
                        "parcelNumber": parcelNumber,
                        "bank": bank,
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

                    self._valuesOfFile.append(self._valuesOfLine.copy())

            except Exception as e:
                print(e)

        return self._valuesOfFile

if __name__ == "__main__":
    paymentsWinthorPDF = PaymentsWinthorPDF()
    paymentDates = paymentsWinthorPDF.returnPaymentsDates("C:/_temp/integracao_diviart/teste.txt")

    paymentsWinthorExcel = PaymentsWinthorExcel()
    paymentsWinthorExcel.readValuesOfBank(os.path.join(fileDir, 'backend/accounting_integration/data/1428_banks.json'))
    print(paymentsWinthorExcel.processPayments("C:/_temp/integracao_diviart/Contas Pagas.xls", paymentDates))

