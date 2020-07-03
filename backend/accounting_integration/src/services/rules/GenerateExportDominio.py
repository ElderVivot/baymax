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

    #  esta função soma o total pago por cada lote, afim de comparar com os extratos bancários posteriormente
    def sumAmountPaidPerLote(self, valuesOfFile):
        amountPaidPerLote = {}
        valuesOfFileWithAmountPaid = []

        for key, currentLine in enumerate(valuesOfFile):
            previousLine = funcoesUteis.analyzeIfFieldIsValidMatrix(valuesOfFile, key-1, {}, True)
            previousLine = {} if key == 0 else previousLine
            previousNumberLote = funcoesUteis.analyzeIfFieldIsValid(previousLine, "numberLote", 0)
            
            currentNumberLote = funcoesUteis.analyzeIfFieldIsValid(currentLine, "numberLote")
            amountPaid = funcoesUteis.analyzeIfFieldIsValid(currentLine, "amountPaid")

            if previousNumberLote == currentNumberLote:
                amountPaidPerLote[currentNumberLote] += amountPaid
            else:
                amountPaidPerLote[currentNumberLote] = amountPaid

        for key, data in enumerate(valuesOfFile):
            numberLote = funcoesUteis.analyzeIfFieldIsValid(data, "numberLote")
            
            data['amountPaidPerLote'] = round(amountPaidPerLote[numberLote], 2)
            valuesOfFileWithAmountPaid.append(data)

        return valuesOfFileWithAmountPaid

    def isPaymentOrExtract(self, data):
        dateTransaction = funcoesUteis.analyzeIfFieldIsValid(data, "dateTransaction", None)
        if dateTransaction is None:
            return "P" # payment pq não existe o dateTransaction
        else:
            return "E"

    def header6000(self):
        idRecord = '6000'
        typeEntry = 'V' # vários débitos pra vários créditos
        codeDefaultEntry = ''
        localizador = ''
        rttFcont = ''

        return f"{idRecord}|{typeEntry}|{codeDefaultEntry}|{localizador}|{rttFcont}|\n"

    def entry6100(self, data, typeData, typeEntry='N', isAmountPaidPerLote=False):
        # o typeData é pra identificar se é débito ou crédito
        # o typeEntry é pra identificar se é um lançamento de juros (J), multa (M), desconto (D) ou normal (N)
        # o isAmountPaidPerLote serve pra pegar o valor do lançamento em vez da chave 'amountPaid' pelo 'amountPaidPerLote'
        paymentOrExtract = self.isPaymentOrExtract(data)
        accountCodeDebit =  ""
        accountCodeCredit = ""

        if paymentOrExtract == "E":
            exportDate = funcoesUteis.transformaCampoDataParaFormatoBrasileiro(funcoesUteis.analyzeIfFieldIsValid(data, "dateTransaction", None))
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
            exportDate = funcoesUteis.transformaCampoDataParaFormatoBrasileiro(funcoesUteis.analyzeIfFieldIsValid(data, "dateOfImport", None))
            amountPaid = funcoesUteis.analyzeIfFieldIsValid(data, "amountPaid", 0.0)
            amountPaidPerLote = funcoesUteis.analyzeIfFieldIsValid(data, "amountPaidPerLote", 0.0)
            amountPaidPerLoteOriginal = amountPaidPerLote
            if amountPaid < 0: # quando negativo multipla por menos 1, geralmente são os descontos
                amountPaid *= -1
            if amountPaidPerLote < 0:
                amountPaidPerLote *= -1
            if isAmountPaidPerLote is True:
                amountPaid = amountPaidPerLote
            amountDiscount = funcoesUteis.analyzeIfFieldIsValid(data, "amountDiscount", 0.0)
            amountInterest = funcoesUteis.analyzeIfFieldIsValid(data, "amountInterest", 0.0)
            amountFine = funcoesUteis.analyzeIfFieldIsValid(data, "amountFine", 0.0)
            amountLiquid = amountPaid - amountInterest - amountFine + amountDiscount

            if typeEntry == 'N':
                if typeData == 'D':
                    accountCodeDebit = funcoesUteis.analyzeIfFieldIsValid(data, "accountCode", "")
                    amount = amountLiquid
                else:
                    if isAmountPaidPerLote is True: 
                        if amountPaidPerLoteOriginal < 0: # se for o total do lote então o crédito é o banco se o valor for maior que zero, se não é débito
                            accountCodeDebit = funcoesUteis.analyzeIfFieldIsValid(data, "accountCodeBank", "")
                        else:
                            accountCodeCredit = funcoesUteis.analyzeIfFieldIsValid(data, "accountCodeBank", "")
                    else: # se não for o total do lote e for lançamento de crédito então provavelmente são os descontos
                        accountCodeCredit = funcoesUteis.analyzeIfFieldIsValid(data, "accountCode", "")
                    amount = amountPaid
                historicCode = funcoesUteis.analyzeIfFieldIsValid(data, "historicCodePagamento", 0)
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

            historic = ""
            compositionHistoric = funcoesUteis.analyzeIfFieldIsValid(data, "compositionHistoric")
            compositionHistoricSplit = compositionHistoric.split('-')
            if compositionHistoric == "":
                if document != "" and document != "0":
                    historic = f"PAGAMENTO CFE. NF/DUP {document} REFERENTE {nameProvider}{historicTemp}"
                else:
                    historic = f"PAGAMENTO REFERENTE {nameProvider}{historicTemp}"
            else:
                for value in compositionHistoricSplit:
                    if value.find('historicCode') >= 0:
                        continue

                    historic += f'{funcoesUteis.analyzeIfFieldIsValid(data, value)} '
                historic = historic.strip()

            # mudo o histórico pois num pagamento em lote (diferentes fornecedores e mesmo banco) não pode vir a informação do fornecedor, pois cada pagamento é um diferente
            amountPaidOriginal = funcoesUteis.analyzeIfFieldIsValid(data, "amountPaid", 0.0)
            amountPaidPerLote = funcoesUteis.analyzeIfFieldIsValid(data, "amountPaidPerLote", 0.0)
            if isAmountPaidPerLote is True and amountPaidOriginal != amountPaidPerLote:
                historicCode = funcoesUteis.analyzeIfFieldIsValid(data, "historicCodePagamento", 0)
                historic = "PAGAMENTO" if historicCode == 0 else ""

            # se não achar na configuração o código do histórico mas estiver configurado pra impotar histórico manipulado seta como zero
            if compositionHistoricSplit != "" and compositionHistoricSplit.count('historicCodePagamento') == 0 and typeEntry == 'N':
                historicCode = 0

        branch = funcoesUteis.analyzeIfFieldIsValid(data, "companyBranch", self._codiEmp)

        idRecord = '6100'
        user = ""
        scp = ""

        if amountFloat > 0:
            return f"{idRecord}|{exportDate}|{accountCodeDebit}|{accountCodeCredit}|{amount}|{historicCode}|{historic}|{user}|{branch}|{scp}|\n"
        else:
            return ""

    # def entry6100PaymentsAmountOfBank(self):

    def exportExtracts(self):
        for key, extract in enumerate(self._extracts):
            accountCodeDebit = funcoesUteis.treatNumberField(funcoesUteis.analyzeIfFieldIsValid(extract, "accountCodeDebit"), isInt=True)
            accountCodeCredit = funcoesUteis.treatNumberField(funcoesUteis.analyzeIfFieldIsValid(extract, "accountCodeCredit"), isInt=True)
            operation = funcoesUteis.analyzeIfFieldIsValid(extract, "operation")
            
            
            if accountCodeDebit > 0 and accountCodeCredit > 0:
                self._file.write(self.header6000())
                self._file.write(self.entry6100(extract, 'D'))
                self._file.write(self.entry6100(extract, 'C'))
                
    def exportPayments(self):

        numberLotesProcessed = []

        try:
            payments = sorted(self._payments, key=itemgetter('numberLote'))
        except Exception:
            payments = self._payments

        payments = self.sumAmountPaidPerLote(payments)

        for key, payment in enumerate(payments):
            accountCodeDebit = funcoesUteis.treatNumberField(funcoesUteis.analyzeIfFieldIsValid(payment, "accountCode"), isInt=True)
            accountCodeCredit = funcoesUteis.treatNumberField(funcoesUteis.analyzeIfFieldIsValid(payment, "accountCodeBank", 0), isInt=True)
            amountPaid = funcoesUteis.analyzeIfFieldIsValid(payment, "amountPaid", 0)
            numberLote = funcoesUteis.analyzeIfFieldIsValid(payment, "numberLote")
            
            if accountCodeDebit > 0 and accountCodeCredit > 0:

                # somente gera o cabeçalho e o total do lote caso ainda não tenha processado aquele 'numberLote'
                if numberLotesProcessed.count(numberLote) == 0:
                    self._file.write(self.header6000())
                    self._file.write(self.entry6100(payment, 'C', 'N', isAmountPaidPerLote=True))
                    numberLotesProcessed.append(numberLote)
                
                if amountPaid > 0:
                    self._file.write(self.entry6100(payment, 'D', 'N'))
                else:
                    self._file.write(self.entry6100(payment, 'C', 'N')) # os negativos tenho que creditar, geralmente são os descontos
                
                self._file.write(self.entry6100(payment, 'D', 'J'))
                self._file.write(self.entry6100(payment, 'D', 'M'))
                self._file.write(self.entry6100(payment, 'C', 'D'))

    def closeFile(self):
        self._file.close()
