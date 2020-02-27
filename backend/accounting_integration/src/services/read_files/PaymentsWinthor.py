import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import json
from tools.leArquivos import leXls_Xlsx, leTxt, readJson
import tools.funcoesUteis as funcoesUteis


class PaymentsWinthorPDF(object):
    def __init__(self, wayTemp):
        self._wayTemp = wayTemp
        self._paymentsDate = []
        self._wayTempFilesRead = os.path.join(wayTemp, 'FilesReads.json')

    def isPaymentWinthorPDF(self, file):
        dataFile = leTxt(file)

        for data in dataFile:
            data = str(data).strip()
            data = funcoesUteis.treatTextField(data)

            fieldsSeparatedBySpace = data.split(' ')

            count = 0
            for valueOfField in fieldsSeparatedBySpace:
                if valueOfField in ("718", "CONTAS", "PAGAS"):
                    count += 1
            
            if count == 3:
                return True

    def process(self, file):
        # se não for desta classe nem segue pra frente
        if self.isPaymentWinthorPDF(file) is None:
            return {}

        funcoesUteis.updateFilesRead(self._wayTempFilesRead, file.replace('.txt', '.pdf'), 'PaymentsWinthorPDF')

        valuesPaymentDates = {}
        valuesOfLine = []
        paymentDate = None

        dataFile = leTxt(file)

        # primeiro percorre e divide cada campo separando por um espaço
        for data in dataFile:
            data = str(data).strip()
            data = funcoesUteis.treatTextField(data)

            fieldsSeparatedBySpace = data.split(' ')

            valuesOfLine.append(fieldsSeparatedBySpace)

        # percorre os campos ajustados e faz o tratamento
        for key, valueOfLine in enumerate(valuesOfLine):
            try:
                if valueOfLine[0] == "DT.PAGAMENTO:":
                    paymentDate = funcoesUteis.transformaCampoDataParaFormatoBrasileiro(\
                        funcoesUteis.retornaCampoComoData(valueOfLine[1]))

                if valueOfLine[0] == "DT." and valueOfLine[1] == "PAGAMENTO:":
                    paymentDate = funcoesUteis.transformaCampoDataParaFormatoBrasileiro(\
                        funcoesUteis.retornaCampoComoData(valueOfLine[2]))
                    
                # identifica se é uma linha de lançamento com o idLanc devidamente preenchido
                if funcoesUteis.treatNumberField(valueOfLine[0]).isnumeric() and ( valuesOfLine[key+1][0] == "HISTORICO" or ( valueOfLine[1].isnumeric() and valueOfLine[2].isnumeric() ) ):
                    valuesPaymentDates[valueOfLine[0]] = paymentDate

            except Exception as e:
                pass
        
        return valuesPaymentDates

    def processAll(self):
        for root, dirs, files in os.walk(self._wayTemp):
            for file in files:
                if file.lower().endswith(('.txt')):
                    wayFile = os.path.join(root, file)
                    self._paymentsDate.append(self.process(wayFile))

        return funcoesUteis.removeAnDictionaryFromWithinArray(self._paymentsDate)


class PaymentsWinthorExcel(object):

    def __init__(self, codiEmp, wayOriginalToRead, wayTemp, settings):
        self._codiEmp = codiEmp
        self._wayOriginalToRead = wayOriginalToRead
        self._wayTemp = wayTemp
        self._payments = []
        self._wayTempFilesRead = os.path.join(wayTemp, 'FilesReads.json')
        self._settings = settings

        # decla a leitura dos PaymentsWinthor PDF
        paymentsWinthorPDF = PaymentsWinthorPDF(self._wayTemp)
        self._paymentsDate = paymentsWinthorPDF.processAll()

    def isPayment(self, file):
        dataFile = leXls_Xlsx(file)

        for data in dataFile:
            textHistoric = funcoesUteis.treatTextFieldInVector(data, 2)

            textUser = funcoesUteis.treatTextFieldInVector(data, 8)

            if textHistoric == "HISTORICO" and ( textUser == "USU.LANC." or textUser == "USU. LANC." ):
                return True
        
    # backend/accounting_integration/data
    def returnBank(self, numberBank):
        try:
            self._banks = self._settings["financy"]["banksConfiguration"]
            bank = self._banks[str(numberBank)].split(' ')
            return bank
        except Exception:
            return ""

    def process(self, file):
        # se não for desta classe nem segue pra frente
        # if self.isPayment(file) is None:
        #     return []

        funcoesUteis.updateFilesRead(self._wayTempFilesRead, file.replace('.txt', '.pdf'), 'PaymentsWinthorExcel')

        dataFile = leXls_Xlsx(file)

        valuesOfLine = {}
        valuesOfFile = []

        for key, data in enumerate(dataFile):
            try:
                idLanc = funcoesUteis.treatNumberFieldInVector(data, 1)

                # paymentDate = self._paymentsDate[idLanc]
                paymentDate = funcoesUteis.treatDateFieldInVector(data, 18)

                nameProvider = funcoesUteis.treatTextFieldInVector(data, 4)

                document = funcoesUteis.treatTextFieldInVector(data, 5)

                accountPlan = funcoesUteis.treatTextFieldInVector(data, 2)
                # juros e desconto sai repetido no relatório do cliente, pois já vem na coluna de juros e multa, então ignoro
                if accountPlan == "MULTA E JUROS DE MORA" or accountPlan == "DESCONTOS OBTIDOS":
                    continue

                historic = "" # funcoesUteis.treatTextFieldInVector(data, 4)
                # if paymentDate is not None and historic == "":
                #     historic = funcoesUteis.treatTextFieldInVector(dataFile[key+1], 4)

                parcelNumber = funcoesUteis.treatNumberFieldInVector(data, 7)

                amountPaid = funcoesUteis.treatDecimalFieldInVector(data, 12)

                amountDevolution = funcoesUteis.treatDecimalFieldInVector(data, 9)

                amountDiscount = funcoesUteis.treatDecimalFieldInVector(data, 10)

                amountInterest = funcoesUteis.treatDecimalFieldInVector(data, 11)

                amountOriginal = funcoesUteis.treatDecimalFieldInVector(data, 8)

                if amountOriginal == amountPaid and amountOriginal > 0:
                    amountPaid = amountPaid + amountInterest - amountDiscount

                paymentType = funcoesUteis.treatTextFieldInVector(data, 13)

                bank = funcoesUteis.treatTextFieldInVector(data, 14)
                bankVector = self.returnBank(bank)
                bank = funcoesUteis.treatTextFieldInVector(bankVector, 1)

                account = funcoesUteis.treatTextFieldInVector(bankVector, 2)

                companyBranch = funcoesUteis.treatTextFieldInVector(data, 18)

                if paymentDate is not None and amountPaid != 0:
                    valuesOfLine = {
                        "paymentDate": paymentDate,
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

    # paymentsWinthorExcel = PaymentsWinthorExcel()
    # print(paymentsWinthorExcel.processPayments("C:/_temp/integracao_diviart/Contas Pagas.xls", paymentDates))

