import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import json
from tools.leArquivos import leXls_Xlsx, leTxt
import tools.funcoesUteis as funcoesUteis


class PaymentsCDI(object):

    def __init__(self):
        self._valuesOfLine = {}
        self._valuesOfFile = []
        self._posionsOfHeader = {}

    def processPayments(self, file):
        dataFile = leXls_Xlsx(file)

        for key, data in enumerate(dataFile):

            try:
                if str(data[0]).upper().count('SEQ') > 0:
                    self._posionsOfHeader.clear()
                    for keyField, nameField in enumerate(data):
                        nameField = funcoesUteis.treatTextField(nameField)
                        self._posionsOfHeader[nameField] = keyField
                    continue

                paymentDate = funcoesUteis.treatDateFieldInVector(data, fieldsHeader=self._posionsOfHeader, nameFieldHeader="Data")

                nameProviderOriginal = funcoesUteis.treatTextFieldInVector(data, fieldsHeader=self._posionsOfHeader, nameFieldHeader="Conta")
                nameProviderSplit = nameProviderOriginal.split('-')
                nameProvider = ""
                for i in range(1, len(nameProviderSplit)):
                    nameProvider = f"{nameProvider} {nameProviderSplit[i]}"
                nameProvider = funcoesUteis.minimalizeSpaces(nameProvider)

                document = funcoesUteis.treatTextFieldInVector(data, fieldsHeader=self._posionsOfHeader, nameFieldHeader="Documento")

                historic = funcoesUteis.treatTextFieldInVector(data, fieldsHeader=self._posionsOfHeader, nameFieldHeader="Descricao")

                amountPaid = funcoesUteis.treatDecimalFieldInVector(data, fieldsHeader=self._posionsOfHeader, nameFieldHeader="Valor Previsto")

                if paymentDate is not None and amountPaid > 0:
                    self._valuesOfLine = {
                        "paymentDate": funcoesUteis.transformaCampoDataParaFormatoBrasileiro(paymentDate),
                        "nameProvider": nameProvider,
                        "document": document,
                        "amountPaid": amountPaid,
                        "historic": historic
                    }

                    self._valuesOfFile.append(self._valuesOfLine.copy())

            except Exception as e:
                print(e)

        return self._valuesOfFile

if __name__ == "__main__":
    paymentsCDI = PaymentsCDI()
    print(paymentsCDI.processPayments("C:/_temp/integracao_diviart/angio.xlsx"))

