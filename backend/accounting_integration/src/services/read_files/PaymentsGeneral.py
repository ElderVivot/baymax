import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import json
from tools.leArquivos import leXls_Xlsx, leTxt, readJson
import tools.funcoesUteis as funcoesUteis
from dao.src.ConnectMongo import ConnectMongo


class PaymentsGeneral(object):

    def __init__(self, codiEmp, wayOriginalToRead, wayTemp):
        self._codiEmp = codiEmp
        self._wayOriginalToRead = wayOriginalToRead
        self._wayTemp = wayTemp
        self._payments = []

        self._connectionMongo = ConnectMongo()
        self._dbMongo = self._connectionMongo.getConnetion()
        self._collection = self._dbMongo.IntegrattionCompanies

    # def isPayment(self, file):
    #     dataFile = leXls_Xlsx(file)

    #     for data in dataFile:
    #         textComparateOne = funcoesUteis.treatTextFieldInVector(data, 2)

    #         textCompara = funcoesUteis.treatTextFieldInVector(data, 8)

    #         if textHistoric == "HISTORICO" and ( textUser == "USU.LANC." or textUser == "USU. LANC." ):
    #             return True
    
    def settingsLayouts(self):
        settings = self._collection.aggregate([
            { "$match": {"codi_emp": self._codiEmp} },
            { "$lookup": {
                "from": "IntegrattionLayouts",
                "localField": "idLayout",
                "foreignField": "IntegrattionLayouts._id",
                "as": "layoutSettings"
            }},
            { "$project": { "layoutSettings": 1, "_id": 0 }}
        ])

        return settings

    def process(self, file):
        settingsLayouts = self.settingsLayouts()

        if settingsLayouts is None:
            return None

        for setting in settingsLayouts:
            print(setting)

        # dataFile = leXls_Xlsx(file)

        # valuesOfLine = {}
        # valuesOfFile = []
        # posionsOfHeader = {}

        # for key, data in enumerate(dataFile):

        #     try:
        #         for field in data:
        #             if funcoesUteis.treatTextField(field)
        #         fieldTwo = funcoesUteis.treatTextFieldInVector(data, 2)
        #         fieldThree = funcoesUteis.treatTextFieldInVector(data, 3)
        #         if fieldTwo.count('NRO NOTA') > 0 or fieldThree.count('NRO NOTA') > 0:
        #             posionsOfHeader.clear()
        #             for keyField, nameField in enumerate(data):
        #                 nameField = funcoesUteis.treatTextField(nameField)
        #                 posionsOfHeader[nameField] = keyField
        #             continue

        #         paymentDate = funcoesUteis.retornaCampoComoData(funcoesUteis.treatTextFieldInVector(data, 11, posionsOfHeader, "Data Baixa"))
        #         nameProvider = funcoesUteis.treatTextFieldInVector(data, 4, posionsOfHeader, "Nome Parceiro")
        #         cgceProvider = funcoesUteis.treatTextFieldInVector(data, 114, posionsOfHeader, "CNPJ / CPF (Parceiro)")
        #         document = funcoesUteis.treatTextFieldInVector(data, 3, posionsOfHeader, "Nro Nota")
        #         accountPlan = funcoesUteis.treatTextFieldInVector(data, 7, posionsOfHeader, "Descricao (Natureza)")
        #         dueDate = funcoesUteis.retornaCampoComoData(funcoesUteis.treatTextFieldInVector(data, 5, posionsOfHeader, "Dt. Vencimento"))
        #         issueDate = funcoesUteis.retornaCampoComoData(funcoesUteis.treatTextFieldInVector(data, 59, posionsOfHeader, "Dt. Entrada e Saída"))
        #         historic = ""
        #         parcelNumber = ""
        #         amountPaid = funcoesUteis.treatDecimalFieldInVector(data, 19, posionsOfHeader, "Vlr Baixa")
        #         amountDevolution = funcoesUteis.treatDecimalFieldInVector(0.0)
        #         amountDiscount = funcoesUteis.treatDecimalFieldInVector(data, 41, posionsOfHeader, "Vlr Desconto")
        #         amountInterest = funcoesUteis.treatDecimalFieldInVector(data, 44, posionsOfHeader, "Vlr Juros")
        #         amountFine = funcoesUteis.treatDecimalFieldInVector(data, 45, posionsOfHeader, "Vlr Multa")
        #         amountOriginal = float(0)
        #         paymentType = ""
        #         bank = funcoesUteis.treatTextFieldInVector(data, 53, posionsOfHeader, "Conta Bancaria")
        #         account = ""
        #         companyBranch = ""

        #         generateDataOnlyIfBankIsInTheConfiguration = funcoesUteis.returnDataFieldInDict(self._settings, ["financy", "generateDataOnlyIfBankIsInTheConfiguration"])

        #         bankVector = self.returnBank(bank)
        #         bank = funcoesUteis.treatTextFieldInVector(bankVector, 1)

        #         if generateDataOnlyIfBankIsInTheConfiguration is True and bankVector == "":
        #             continue

        #         account = funcoesUteis.treatTextFieldInVector(bankVector, 2)

        #         if paymentDate is not None and amountPaid > 0:
        #             valuesOfLine = {
        #                 "paymentDate": funcoesUteis.transformaCampoDataParaFormatoBrasileiro(paymentDate),
        #                 "nameProvider": nameProvider,
        #                 "cgceProvider": cgceProvider,
        #                 "document": document,
        #                 "parcelNumber": parcelNumber,
        #                 "bank": bank,
        #                 "account": account,
        #                 "dueDate": dueDate,
        #                 "issueDate": issueDate,
        #                 "amountPaid": amountPaid,
        #                 "amountDiscount": amountDiscount,
        #                 "amountInterest": amountInterest,
        #                 "amountOriginal": amountOriginal,
        #                 "amountFine": amountFine,
        #                 "amountDevolution": amountDevolution,
        #                 "paymentType": paymentType,
        #                 "accountPlan": accountPlan,
        #                 "historic": historic,
        #                 "companyBranch": companyBranch
        #             }

        #             valuesOfFile.append(valuesOfLine.copy())

            # except Exception as e:
            #     pass

        return 0 #valuesOfFile

    def processAll(self):
        for root, dirs, files in os.walk(self._wayOriginalToRead):
            for file in files:
                wayFile = os.path.join(root, file)

                if file.lower().endswith(('.xls', '.xlsx')):
                    self._payments.append(self.process(wayFile))

        return funcoesUteis.removeAnArrayFromWithinAnother(self._payments)

if __name__ == "__main__":

    payments = PaymentsGeneral(1117, "C:/integracao_contabil/1117/arquivos_originais", "")
    payments.processAll()

