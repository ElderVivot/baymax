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
        self._extracts = []

    def getPayments(self):
        dataFile = leXls_Xlsx(self._file, 'Pagamentos')

        for data in dataFile:
            if str(data[0]).upper().count('DOCUMENTO') > 0:
                    self._posionsOfHeaderPayments.clear()
                    for keyField, nameField in enumerate(data):
                        nameField = funcoesUteis.treatTextField(nameField)
                        self._posionsOfHeaderPayments[nameField] = keyField
                    continue

            document = funcoesUteis.treatTextFieldInVector(data, )
            findNote = funcoesUteis.analyzeIfFieldIsValid(payment, "findNote")
            parcelNumber = funcoesUteis.analyzeIfFieldIsValid(payment, "parcelNumber")
            nameProvider = funcoesUteis.analyzeIfFieldIsValid(payment, "nameProvider")
            cgceProvider = funcoesUteis.analyzeIfFieldIsValid(payment, "cgceProvider")
            bankAndAccount = f'{funcoesUteis.analyzeIfFieldIsValid(payment, "bank")}-{funcoesUteis.analyzeIfFieldIsValid(payment, "account")}'
            bankAndAccountExtract = f'{funcoesUteis.analyzeIfFieldIsValid(payment, "bankExtract")}-{funcoesUteis.analyzeIfFieldIsValid(payment, "accountExtract")}'
            foundProof = funcoesUteis.analyzeIfFieldIsValid(payment, "foundProof")
            paymentDate = funcoesUteis.retornaCampoComoData(funcoesUteis.analyzeIfFieldIsValid(payment, "paymentDate", None))
            extractDate = funcoesUteis.retornaCampoComoData(funcoesUteis.analyzeIfFieldIsValid(payment, "dateExtract", None))
            dateOfImport = funcoesUteis.retornaCampoComoData(funcoesUteis.analyzeIfFieldIsValid(payment, "dateOfImport", None))
            dueDate = funcoesUteis.retornaCampoComoData(funcoesUteis.analyzeIfFieldIsValid(payment, "dueDate"))
            issueDate = funcoesUteis.retornaCampoComoData(funcoesUteis.analyzeIfFieldIsValid(payment, "issueDate"))
            amountPaid = funcoesUteis.analyzeIfFieldIsValid(payment, "amountPaid")
            amountDiscount = funcoesUteis.analyzeIfFieldIsValid(payment, "amountDiscount")
            amountInterest = funcoesUteis.analyzeIfFieldIsValid(payment, "amountInterest")
            amountFine = funcoesUteis.analyzeIfFieldIsValid(payment, "amountFine")
            amountOriginal = funcoesUteis.analyzeIfFieldIsValid(payment, "amountOriginal")
            accountCode = funcoesUteis.analyzeIfFieldIsValid(payment, "accountCode")
            codiEmp = funcoesUteis.analyzeIfFieldIsValid(payment, "codiEmp")
            historic = funcoesUteis.analyzeIfFieldIsValid(payment, "historic")
            category = funcoesUteis.analyzeIfFieldIsValid(payment, "category")
            accountPlan = funcoesUteis.analyzeIfFieldIsValid(payment, "accountPlan")
            paymentType = funcoesUteis.analyzeIfFieldIsValid(payment, "paymentType")
            historicExtract = funcoesUteis.analyzeIfFieldIsValid(payment, "historicExtract")