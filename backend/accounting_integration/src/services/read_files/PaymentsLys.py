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
                        bank = bankAndAccount[ positionWordBank+5 : positionPlusSign ]
                        print(bank)
                    else:
                        bank = "DINHEIRO"
                        accountBank = ""

                    if paymentDate is not None:
                        self._valuesOfLine = {
                            "idAccountPaid": idAccountPaid,
                            "paymentDate": funcoesUteis.transformaCampoDataParaFormatoBrasileiro(paymentDate),
                            "bankAndAccount": bankAndAccount,
                            "accountCode": accountCode,
                        }

                        self._valuesOfFile.append(self._valuesOfLine.copy())
                except Exception:
                    pass

            return self._valuesOfFile


if __name__ == "__main__":
    paymentsLysPorMoeda = PaymentsLysPorMoeda("C:/integracao_contabil/1777/arquivos_originais/LD POR MOEDA.XLS")
    print(paymentsLysPorMoeda.process())
