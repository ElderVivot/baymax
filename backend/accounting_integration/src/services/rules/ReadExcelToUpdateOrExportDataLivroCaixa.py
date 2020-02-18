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
        self._dataOfLine = {}
        self._dataOfFile = []
        self._posionsOfHeader = {}

        self._dataOfLineAccountPlan = {}
        self._dataOfFileAccountPlan = []
        self._posionsOfHeaderAccountPlan = {}

    def getLivroCaixa(self):
        dataFile = leXls_Xlsx(self._file, 'Lancamentos')

        for data in dataFile:
            if str(data[0]).upper().count('DOCUMENTO') > 0:
                self._posionsOfHeader.clear()
                for keyField, nameField in enumerate(data):
                    nameField = funcoesUteis.treatTextField(nameField)
                    self._posionsOfHeader[nameField] = keyField
                continue

            dateLivro = funcoesUteis.treatDateFieldInVector(data, 1, self._posionsOfHeader, "Data")
            movementType = funcoesUteis.treatTextFieldInVector(data, 2, self._posionsOfHeader, "Tipo Movimento")
            account = funcoesUteis.treatTextFieldInVector(data, 3, self._posionsOfHeader, "Conta Contábil")
            nameAccount = funcoesUteis.treatTextFieldInVector(data, 4, self._posionsOfHeader, "Nome Conta")
            amount = funcoesUteis.treatDecimalFieldInVector(data, 5, self._posionsOfHeader, "Valor")
            document = funcoesUteis.treatTextFieldInVector(data, 6, self._posionsOfHeader, "Documento")
            documentType = funcoesUteis.treatTextFieldInVector(data, 7, self._posionsOfHeader, "Tipo Documento")
            participante = funcoesUteis.treatTextFieldInVector(data, 8, self._posionsOfHeader, "Participante")
            imovelRural = funcoesUteis.treatTextFieldInVector(data, 9, self._posionsOfHeader, "Imóvel Rural")
            historic = funcoesUteis.treatTextFieldInVector(data, 10, self._posionsOfHeader, "Histórico")

            if amount != 0:
                self._dataOfLine = {
                    'dateLivro': dateLivro,
                    'movementType':movementType,
                    'account': account,
                    'nameAccount': nameAccount,
                    'amount': amount,
                    'document': document,
                    'documentType': documentType,
                    'participante': participante,
                    'imovelRural': imovelRural,
                    'historic': historic
                }

                self._dataOfFile.append(self._dataOfLine.copy())

        return self._dataOfFile

    def getAccountPlan(self):
        dataFile = leXls_Xlsx(self._file, 'PlanoContas')

        for data in dataFile:
            if str(data[0]).upper().count('CONTA') > 0:
                self._posionsOfHeaderAccountPlan.clear()
                for keyField, nameField in enumerate(data):
                    nameField = funcoesUteis.treatTextField(nameField)
                    self._posionsOfHeaderAccountPlan[nameField] = keyField
                continue

            dateLivro = funcoesUteis.treatDateFieldInVector(data, 1, self._posionsOfHeader, "Data")
            movementType = funcoesUteis.treatTextFieldInVector(data, 2, self._posionsOfHeader, "Tipo Movimento")
            account = funcoesUteis.treatTextFieldInVector(data, 3, self._posionsOfHeader, "Conta Contábil")
            nameAccount = funcoesUteis.treatTextFieldInVector(data, 4, self._posionsOfHeader, "Nome Conta")
            amount = funcoesUteis.treatDecimalFieldInVector(data, 5, self._posionsOfHeader, "Valor")
            document = funcoesUteis.treatTextFieldInVector(data, 6, self._posionsOfHeader, "Documento")
            documentType = funcoesUteis.treatTextFieldInVector(data, 7, self._posionsOfHeader, "Tipo Documento")
            participante = funcoesUteis.treatTextFieldInVector(data, 8, self._posionsOfHeader, "Participante")
            imovelRural = funcoesUteis.treatTextFieldInVector(data, 9, self._posionsOfHeader, "Imóvel Rural")
            historic = funcoesUteis.treatTextFieldInVector(data, 10, self._posionsOfHeader, "Histórico")

            if amount != 0:
                self._dataOfLine = {
                    'dateLivro': dateLivro,
                    'movementType':movementType,
                    'account': account,
                    'nameAccount': nameAccount,
                    'amount': amount,
                    'document': document,
                    'documentType': documentType,
                    'participante': participante,
                    'imovelRural': imovelRural,
                    'historic': historic
                }

                self._dataOfFile.append(self._dataOfLine.copy())

        return self._dataOfFile