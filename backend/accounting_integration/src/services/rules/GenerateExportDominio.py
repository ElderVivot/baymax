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

        return f"{idRecord}|{typeEntry}|{codeDefaultEntry}|{localizador}|{rttFcont}|\n"

    def entry6100(self, data, typeData, typeEntry='N'):
        # o typeData é pra identificar se é débito ou crédito
        # o typeEntry é pra identificar se é um lançamento de juros (J), multa (M), desconto (D) ou normal (N)
        paymentOrExtract = self.isPaymentOrExtract(data)
        accountCodeDebit =  ""
        accountCodeCredit = ""

        if paymentOrExtract == "E":
            exportDate = funcoesUteis.analyzeIfFieldIsValid(data, "dateTransaction", None)
            if typeData == 'D':
                accountCodeDebit = funcoesUteis.analyzeIfFieldIsValid(data, "accountCodeDebit", "")
            else:
                accountCodeCredit = funcoesUteis.analyzeIfFieldIsValid(data, "accountCodeCredit", "")
            amount = funcoesUteis.analyzeIfFieldIsValid(data, "amount", 0.0)
            amountFloat = amount
            amount = str(amount).replace('.', ',')
            historicCode = funcoesUteis.analyzeIfFieldIsValid(data, "historicCode", "")
            historic = funcoesUteis.analyzeIfFieldIsValid(data, "historic", "")

        elif paymentOrExtract == "P":
            exportDate = funcoesUteis.analyzeIfFieldIsValid(data, "dateOfImport", None)
            amountPaid = funcoesUteis.analyzeIfFieldIsValid(data, "amountPaid", 0.0)
            amountDiscount = funcoesUteis.analyzeIfFieldIsValid(data, "amountDiscount", 0.0)
            amountInterest = funcoesUteis.analyzeIfFieldIsValid(data, "amountInterest", 0.0)
            amountFine = funcoesUteis.analyzeIfFieldIsValid(data, "amountFine", 0.0)
            amountLiquid = amountPaid - amountInterest - amountFine + amountDiscount

            if typeEntry == 'N':
                if typeData == 'D':
                    accountCodeDebit = funcoesUteis.analyzeIfFieldIsValid(data, "accountCode", "")
                    amount = amountLiquid
                else:
                    accountCodeCredit = funcoesUteis.analyzeIfFieldIsValid(data, "accountCodeBank", "")
                    amount = amountPaid
                historicCode = 15
            elif typeEntry == 'J':
                accountCodeDebit = funcoesUteis.analyzeIfFieldIsValid(data, "accountCodeInterest", 372)
                historicCode = funcoesUteis.analyzeIfFieldIsValid(data, "historicCodeInterest", 26)
                amount = funcoesUteis.analyzeIfFieldIsValid(data, "amountInterest", 0.0)
            elif typeEntry == 'M':
                accountCodeDebit = funcoesUteis.analyzeIfFieldIsValid(data, "accountCodeFine", 352)
                historicCode = funcoesUteis.analyzeIfFieldIsValid(data, "historicCodeFine", 25)
                amount = funcoesUteis.analyzeIfFieldIsValid(data, "amountFine", 0.0)
            elif typeEntry == 'D':
                accountCodeCredit = funcoesUteis.analyzeIfFieldIsValid(data, "accountCodeDiscount", 434)
                historicCode = funcoesUteis.analyzeIfFieldIsValid(data, "historicCodeDiscount", 28)
                amount = funcoesUteis.analyzeIfFieldIsValid(data, "amountDiscount", 0.0)

            amountFloat = amount
            amount = str(amount).replace('.', ',')

            document = funcoesUteis.analyzeIfFieldIsValid(data, "document")
            nameProvider = funcoesUteis.analyzeIfFieldIsValid(data, "nameProvider")

            accountPlan = funcoesUteis.analyzeIfFieldIsValid(data, "accountPlan")
            accountPlan = f" / {accountPlan}" if accountPlan != "" else ""

            historicTemp = funcoesUteis.analyzeIfFieldIsValid(data, "historic")
            historicTemp = f" / {historicTemp}" if historicTemp != "" else accountPlan

            if document != "" and document != "0":
                historic = f"CFE. DUP {document} DO FORNECEDOR {nameProvider}{historicTemp}"
            else:
                historic = f"DO FORNECEDOR {nameProvider}{historicTemp}"

        idRecord = '6100'
        user = ""
        branch = ""
        scp = ""

        if amountFloat > 0:
            return f"{idRecord}|{exportDate}|{accountCodeDebit}|{accountCodeCredit}|{amount}|{historicCode}|{historic}|{user}|{branch}|{scp}|\n"
        else:
            return ""

    def exportExtracts(self):
        for key, extract in enumerate(self._extracts):
            accountCodeDebit = funcoesUteis.treatNumberField(funcoesUteis.analyzeIfFieldIsValid(extract, "accountCodeDebit"), isInt=True)
            accountCodeCredit = funcoesUteis.treatNumberField(funcoesUteis.analyzeIfFieldIsValid(extract, "accountCodeCredit"), isInt=True)
            
            if accountCodeDebit > 0 and accountCodeCredit > 0:
                self._file.write(self.header6000())
                self._file.write(self.entry6100(extract, 'D'))
                self._file.write(self.entry6100(extract, 'C'))
                
    def exportPayments(self):
        for key, payment in enumerate(self._payments):
            accountCodeDebit = funcoesUteis.treatNumberField(funcoesUteis.analyzeIfFieldIsValid(payment, "accountCode"), isInt=True)
            accountCodeCredit = funcoesUteis.treatNumberField(funcoesUteis.analyzeIfFieldIsValid(payment, "accountCodeBank", 0), isInt=True)
            if accountCodeDebit > 0 and accountCodeCredit > 0:
                self._file.write(self.header6000())
                self._file.write(self.entry6100(payment, 'D', 'N'))
                self._file.write(self.entry6100(payment, 'C', 'N'))
                self._file.write(self.entry6100(payment, 'D', 'J'))
                self._file.write(self.entry6100(payment, 'D', 'M'))
                self._file.write(self.entry6100(payment, 'C', 'D'))

    def closeFile(self):
        self._file.close()
