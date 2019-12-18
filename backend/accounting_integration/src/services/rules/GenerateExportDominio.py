import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import json
from datetime import datetime
from operator import itemgetter
import xlsxwriter
import tools.funcoesUteis as funcoesUteis

wayToSaveFiles = open(os.path.join(fileDir, 'backend/accounting_integration/src/WayToSaveFiles.json') )
wayDefault = json.load(wayToSaveFiles)
wayToSaveFiles.close()


class GenerateExportDominio(object):

    def __init__(self, codiEmp, nameFileExport, payments=[], extracts=[]):
        self._codiEmp = codiEmp

        self._wayBaseToSaveFiles = os.path.join(wayDefault['WayToSaveFilesOriginals'], f'{self._codiEmp}/arquivos_processados/exportados')
        if os.path.exists(self._wayBaseToSaveFiles) is False:
            os.makedirs(self._wayBaseToSaveFiles)

        self._nameFileExport = f"{funcoesUteis.getOnlyNameFile(nameFileExport)}.txt"
        self._file = open(os.path.join(self._wayBaseToSaveFiles, self._nameFileExport), "w", encoding='utf-8')

        self._payments = payments
        self._extracts = extracts

    def isPaymentOrExtract(self, data):
        bankId = funcoesUteis.analyzeIfFieldIsValid(data, "bankId", None)
        if bankId is None:
            return "P" # payment pq não existe o bankId
        else:
            return "E"

    def header6000(self):
        idRecord = '6000'
        typeEntry = 'V' # vários débitos pra vários créditos
        codeDefaultEntry = ''
        localizador = ''
        rttFcont = ''

        return f"{idRecord}|{typeEntry}|{codeDefaultEntry}|{localizador}|{rttFcont}|"

    def entry6100(self, data, typeEntry):
        paymentOrExtract = self.isPaymentOrExtract(data)

        if paymentOrExtract == "E":
            exportDate = funcoesUteis.analyzeIfFieldIsValid(data, "dateTransaction", None)
            if typeEntry == 'D':
                accountCodeDebit = funcoesUteis.analyzeIfFieldIsValid(data, "accountCodeDebit", "")
                accountCodeCredit = ""
            else:
                accountCodeDebit = ""
                accountCodeCredit = funcoesUteis.analyzeIfFieldIsValid(data, "accountCodeCredit", "")
            amount = funcoesUteis.analyzeIfFieldIsValid(data, "amount", 0.0)
            historicCode = funcoesUteis.analyzeIfFieldIsValid(data, "historicCode", "")
            historic = funcoesUteis.analyzeIfFieldIsValid(data, "historic", "")

        idRecord = '6100'
        user = ""
        branch = ""
        scp = ""

        return f"\n{idRecord}|{exportDate}|{accountCodeDebit}|{accountCodeCredit}|{amount}|{historicCode}|{historic}|{user}|{branch}|{scp}|"

    def exportExtracts(self):
        for extract in self._extracts:
            accountCodeDebit = funcoesUteis.treatNumberFieldInVector(extract, "accountCodeDebit")
            accountCodeCredit = funcoesUteis.treatNumberFieldInVector(extract, "accountCodeCredit")
            if int(accountCodeDebit) > 0 and int(accountCodeCredit) > 0:
                self._file.write(self.header6000())
                self._file.write(self.entry6100(extract, 'D'))
                self._file.write(self.entry6100(extract, 'C'))
            else:
                print(extract)

    def closeFile(self):
        self._file.close()
