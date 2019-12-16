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


class GenerateExcel(object):

    def __init__(self, codiEmp):
        self._codiEmp = codiEmp
        self._wayBaseToSaveFiles = os.path.join(wayDefault['WayToSaveFilesOriginals'], f'{self._codiEmp}/arquivos_processados')
        if os.path.exists(self._wayBaseToSaveFiles) is False:
            os.makedirs(self._wayBaseToSaveFiles)
        self._workbook = xlsxwriter.Workbook(os.path.join(self._wayBaseToSaveFiles, f"integracao_contabil_{self._codiEmp} {funcoesUteis.getDateTimeNowInFormatStr()}.xlsx"))
        self._cell_format_header = self._workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': 'yellow'})
        self._cell_format_money = self._workbook.add_format({'num_format': '##0.00'})
        self._cell_format_date = self._workbook.add_format({'num_format': 'dd/mm/yyyy'})
        
    def sheetExtract(self, extracts):
        sheet = self._workbook.add_worksheet('ExtratosBancarios')

        sheet.write(0, 0, "Data", self._cell_format_header)
        sheet.write(0, 1, "Debito", self._cell_format_header)
        sheet.write(0, 2, "Credito", self._cell_format_header)
        sheet.write(0, 3, "Valor", self._cell_format_header)
        sheet.write(0, 4, "Cod. Hist", self._cell_format_header)
        sheet.write(0, 5, "Historico", self._cell_format_header)
        sheet.write(0, 6, "-------", self._cell_format_header)
        sheet.write(0, 7, "-------", self._cell_format_header)
        sheet.write(0, 8, "Banco", self._cell_format_header)
        sheet.write(0, 9, "Conta Corrente", self._cell_format_header)
        sheet.write(0, 10, "Data Extrato", self._cell_format_header)
        sheet.write(0, 11, "Tipo Transacao", self._cell_format_header)
        sheet.write(0, 12, "Operacao", self._cell_format_header)
        sheet.write(0, 13, "Valor", self._cell_format_header)
        sheet.write(0, 14, "Documento", self._cell_format_header)
        sheet.write(0, 15, "Historico", self._cell_format_header)

        for key, extract in enumerate(extracts):
            row = key+1

            dateExtract = funcoesUteis.retornaCampoComoData(funcoesUteis.analyzeIfFieldIsValid(extract, "dateTransaction"))
            bank = funcoesUteis.analyzeIfFieldIsValid(extract, "bankId")
            account = funcoesUteis.analyzeIfFieldIsValid(extract, "account")
            typeTransaction = funcoesUteis.analyzeIfFieldIsValid(extract, "typeTransaction")
            operation = funcoesUteis.analyzeIfFieldIsValid(extract, "operation")
            document = funcoesUteis.analyzeIfFieldIsValid(extract, "document")
            historic = funcoesUteis.analyzeIfFieldIsValid(extract, "historic")
            amount = funcoesUteis.analyzeIfFieldIsValid(extract, "amount")
            accountCodeDebit = funcoesUteis.analyzeIfFieldIsValid(extract, "accountCodeDebit")
            accountCodeCredit = funcoesUteis.analyzeIfFieldIsValid(extract, "accountCodeCredit")

            if operation == "+":
                historicCode = 24
            else:
                historicCode = 78

            sheet.write(row, 0, dateExtract, self._cell_format_date)
            sheet.write(row, 1, accountCodeDebit)
            sheet.write(row, 2, accountCodeCredit)
            sheet.write(row, 3, amount, self._cell_format_money)
            sheet.write(row, 4, historicCode)
            sheet.write(row, 5, historic)
            sheet.write(row, 6, "")
            sheet.write(row, 7, "")
            sheet.write(row, 8, bank)
            sheet.write(row, 9, account)
            sheet.write(row, 10, dateExtract, self._cell_format_date)
            sheet.write(row, 11, typeTransaction)
            sheet.write(row, 12, operation)
            sheet.write(row, 13, amount, self._cell_format_money)
            sheet.write(row, 14, document)
            sheet.write(row, 15, historic)

        self._workbook.close()

    def sheetPayments(self, payments):
        sheet = self._workbook.add_worksheet('Pagamentos')

        sheet.write(0, 0, "Documento", self._cell_format_header)
        sheet.write(0, 1, "Encontrou a NF na Domínio?", self._cell_format_header)
        sheet.write(0, 2, "Parcela", self._cell_format_header)
        sheet.write(0, 3, "Nome Fornecedor", self._cell_format_header)
        sheet.write(0, 4, "CNPJ Fornecedor", self._cell_format_header)
        sheet.write(0, 5, "Banco Planilha Cliente", self._cell_format_header)
        sheet.write(0, 6, "Banco Extrato", self._cell_format_header)
        sheet.write(0, 7, "Encontrou Comprovante Pagto?", self._cell_format_header)
        sheet.write(0, 8, "Data de Pagto", self._cell_format_header)
        sheet.write(0, 9, "Data do Extrato", self._cell_format_header)
        sheet.write(0, 10, "Data do Lançamento na Domínio", self._cell_format_header)
        sheet.write(0, 11, "Data do Vencimento", self._cell_format_header)
        sheet.write(0, 12, "Data do Emissão", self._cell_format_header)
        sheet.write(0, 13, "Valor Pago", self._cell_format_header)
        sheet.write(0, 14, "Valor Desconto", self._cell_format_header)
        sheet.write(0, 15, "Valor Juros", self._cell_format_header)
        sheet.write(0, 16, "Valor Multa", self._cell_format_header)
        sheet.write(0, 17, "Valor Original", self._cell_format_header)
        sheet.write(0, 18, "Conta Contabil Domínio", self._cell_format_header)
        sheet.write(0, 19, "Codigo Empresa", self._cell_format_header)
        sheet.write(0, 20, "Historico Planilha", self._cell_format_header)
        sheet.write(0, 21, "Categoria", self._cell_format_header)
        sheet.write(0, 22, "Plano de Contas", self._cell_format_header)
        sheet.write(0, 23, "Tipo de Pagamento", self._cell_format_header)
        sheet.write(0, 24, "Historico Extrato Bancário", self._cell_format_header)

        # ordena os payments por data
        payments = sorted(payments, key=itemgetter('dateOfImport'))

        for key, payment in enumerate(payments):
            row = key+1

            document = funcoesUteis.analyzeIfFieldIsValid(payment, "document")
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

            sheet.write(row, 0, document)
            sheet.write(row, 1, findNote)
            sheet.write(row, 2, parcelNumber)
            sheet.write(row, 3, nameProvider)
            sheet.write(row, 4, cgceProvider)
            sheet.write(row, 5, bankAndAccount)
            sheet.write(row, 6, bankAndAccountExtract)
            sheet.write(row, 7, foundProof)
            sheet.write(row, 8, paymentDate, self._cell_format_date)
            sheet.write(row, 9, extractDate, self._cell_format_date)
            sheet.write(row, 10, dateOfImport, self._cell_format_date)
            sheet.write(row, 11, dueDate, self._cell_format_date)
            sheet.write(row, 12, issueDate, self._cell_format_date)
            sheet.write(row, 13, amountPaid, self._cell_format_money)
            sheet.write(row, 14, amountDiscount, self._cell_format_money)
            sheet.write(row, 15, amountInterest, self._cell_format_money)
            sheet.write(row, 16, amountFine, self._cell_format_money)
            sheet.write(row, 17, amountOriginal, self._cell_format_money)
            sheet.write(row, 18, accountCode)
            sheet.write(row, 19, codiEmp)
            sheet.write(row, 20, historic)
            sheet.write(row, 21, category)
            sheet.write(row, 22, accountPlan)
            sheet.write(row, 23, paymentType)
            sheet.write(row, 24, historicExtract)

    def closeFile(self):
        self._workbook.close()
  

# if __name__ == "__main__":
#     generateExcel = GenerateExcel(1428)
#     generateExcel.generateSheetExtract()
