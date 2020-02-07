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

    def __init__(self, codiEmp, update=False, nameFileUpdate=''):
        self._codiEmp = codiEmp

        if update is False:
            self._wayBaseToSaveFiles = os.path.join(wayDefault['WayToSaveFilesOriginals'], f'{self._codiEmp}/arquivos_processados')
        else:
            self._wayBaseToSaveFiles = os.path.join(wayDefault['WayToSaveFilesOriginals'], f'{self._codiEmp}/arquivos_processados/atualizados')

        if os.path.exists(self._wayBaseToSaveFiles) is False:
            os.makedirs(self._wayBaseToSaveFiles)

        if update is False:
            self._workbook = xlsxwriter.Workbook(os.path.join(self._wayBaseToSaveFiles, f"integracao_contabil_{self._codiEmp} {funcoesUteis.getDateTimeNowInFormatStr()}.xlsx"))
        else:
            self._workbook = xlsxwriter.Workbook(os.path.join(self._wayBaseToSaveFiles, f"atualizado_{nameFileUpdate}"))
        
        self._cell_format_header = self._workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': 'yellow'})
        self._cell_format_money = self._workbook.add_format({'num_format': '##0.00'})
        self._cell_format_date = self._workbook.add_format({'num_format': 'dd/mm/yyyy'})
        
    def sheetExtract(self, extracts):
        sheet = self._workbook.add_worksheet('ExtratosBancarios')

        sheet.set_column(11,11,options={'hidden':True})
        sheet.set_column(12,12,options={'hidden':True})
        sheet.set_column(14,16,options={'hidden':True})

        sheet.write(0, 0, "Data", self._cell_format_header)
        sheet.write(0, 1, "Debito", self._cell_format_header)
        sheet.write(0, 2, "Credito", self._cell_format_header)
        sheet.write(0, 3, "Valor", self._cell_format_header)
        sheet.write(0, 4, "Cod. Hist", self._cell_format_header)
        sheet.write(0, 5, "Historico", self._cell_format_header)
        sheet.write(0, 6, "Encontrou no Financeiro?", self._cell_format_header)
        sheet.write(0, 7, "-------", self._cell_format_header)
        sheet.write(0, 8, "-------", self._cell_format_header)
        sheet.write(0, 9, "Banco", self._cell_format_header)
        sheet.write(0, 10, "Conta Corrente", self._cell_format_header)
        sheet.write(0, 11, "Data Extrato", self._cell_format_header)
        sheet.write(0, 12, "Tipo Transacao", self._cell_format_header)
        sheet.write(0, 13, "Operacao", self._cell_format_header)
        sheet.write(0, 14, "Valor Extrato", self._cell_format_header)
        sheet.write(0, 15, "Documento", self._cell_format_header)
        sheet.write(0, 16, "Historico Extrato", self._cell_format_header)

        for key, extract in enumerate(extracts):
            row = key+1

            dateExtract = funcoesUteis.retornaCampoComoData(funcoesUteis.analyzeIfFieldIsValid(extract, "dateTransaction"))
            bank = funcoesUteis.analyzeIfFieldIsValid(extract, "bankId")
            account = funcoesUteis.analyzeIfFieldIsValid(extract, "account")
            typeTransaction = funcoesUteis.analyzeIfFieldIsValid(extract, "typeTransaction")
            operation = funcoesUteis.analyzeIfFieldIsValid(extract, "operation")
            document = funcoesUteis.analyzeIfFieldIsValid(extract, "document")
            historicCode = funcoesUteis.analyzeIfFieldIsValid(extract, "historicCode")
            historic = funcoesUteis.analyzeIfFieldIsValid(extract, "historic")
            amount = funcoesUteis.analyzeIfFieldIsValid(extract, "amount")
            accountCodeDebit = funcoesUteis.analyzeIfFieldIsValid(extract, "accountCodeDebit")
            accountCodeCredit = funcoesUteis.analyzeIfFieldIsValid(extract, "accountCodeCredit")
            foundProofInPayments = funcoesUteis.analyzeIfFieldIsValid(extract, "foundProofInPayments")

            sheet.write(row, 0, dateExtract, self._cell_format_date)
            sheet.write(row, 1, accountCodeDebit)
            sheet.write(row, 2, accountCodeCredit)
            sheet.write(row, 3, amount, self._cell_format_money)
            sheet.write(row, 4, historicCode)
            sheet.write(row, 5, historic)
            sheet.write(row, 6, foundProofInPayments)
            sheet.write(row, 7, "")
            sheet.write(row, 8, "")
            sheet.write(row, 9, bank)
            sheet.write(row, 10, account)
            sheet.write(row, 11, dateExtract, self._cell_format_date)
            sheet.write(row, 12, typeTransaction)
            sheet.write(row, 13, operation)
            sheet.write(row, 14, amount, self._cell_format_money)
            sheet.write(row, 15, document)
            sheet.write(row, 16, historic)

    def sheetPayments(self, payments):
        sheet = self._workbook.add_worksheet('Pagamentos')

        sheet.set_column(2,2,options={'hidden':True}) # parcela
        sheet.set_column(4,4,options={'hidden':True}) # cnpj fornecedor
        sheet.set_column(9,9,options={'hidden':True}) # data extrato
        sheet.set_column(11,11,options={'hidden':True}) # data vencimento
        sheet.set_column(12,12,options={'hidden':True}) # data emissão

        sheet.write(0, 0, "Documento", self._cell_format_header)
        sheet.write(0, 1, "NF na Domínio?", self._cell_format_header)
        sheet.write(0, 2, "Parcela", self._cell_format_header) # hidden
        sheet.write(0, 3, "Fornecedor", self._cell_format_header)
        sheet.write(0, 4, "CNPJ Fornecedor", self._cell_format_header) # hidden
        sheet.write(0, 5, "Banco Financeiro", self._cell_format_header)
        sheet.write(0, 6, "Banco Extrato", self._cell_format_header)
        sheet.write(0, 7, "Comprovante Pagto?", self._cell_format_header)
        sheet.write(0, 8, "Data Financeiro", self._cell_format_header)
        sheet.write(0, 9, "Data Extrato", self._cell_format_header)
        sheet.write(0, 10, "Importação Domínio", self._cell_format_header)
        sheet.write(0, 11, "Vencimento", self._cell_format_header)
        sheet.write(0, 12, "Emissão", self._cell_format_header)
        sheet.write(0, 13, "Valor Pago", self._cell_format_header)
        sheet.write(0, 14, "Desconto", self._cell_format_header)
        sheet.write(0, 15, "Juros", self._cell_format_header)
        sheet.write(0, 16, "Multa", self._cell_format_header)
        sheet.write(0, 17, "Valor Original", self._cell_format_header)
        sheet.write(0, 18, "Conta Contabil Domínio", self._cell_format_header)
        sheet.write(0, 19, "Codigo Empresa", self._cell_format_header)
        sheet.write(0, 20, "Historico Financeiro", self._cell_format_header)
        sheet.write(0, 21, "Categoria", self._cell_format_header)
        sheet.write(0, 22, "Plano de Contas", self._cell_format_header)
        sheet.write(0, 23, "CNPJ Pagador", self._cell_format_header)
        sheet.write(0, 24, "Historico Extrato Bancário", self._cell_format_header)
        sheet.write(0, 25, "Conta Contabil Sistema Cliente", self._cell_format_header)

        # ordena os payments por data
        payments = sorted(payments, key=itemgetter('bank', 'dateOfImport'))

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
            dateOfImport = funcoesUteis.analyzeIfFieldIsValid(payment, "dateOfImport", None)
            dueDate = funcoesUteis.retornaCampoComoData(funcoesUteis.analyzeIfFieldIsValid(payment, "dueDate"))
            issueDate = funcoesUteis.retornaCampoComoData(funcoesUteis.analyzeIfFieldIsValid(payment, "issueDate"))
            amountPaid = funcoesUteis.analyzeIfFieldIsValid(payment, "amountPaid")
            amountDiscount = funcoesUteis.analyzeIfFieldIsValid(payment, "amountDiscount", 0.0)
            amountInterest = funcoesUteis.analyzeIfFieldIsValid(payment, "amountInterest", 0.0)
            amountFine = funcoesUteis.analyzeIfFieldIsValid(payment, "amountFine", 0.0)
            amountOriginal = funcoesUteis.analyzeIfFieldIsValid(payment, "amountOriginal", 0.0)
            accountCode = funcoesUteis.analyzeIfFieldIsValid(payment, "accountCode")
            codiEmp = funcoesUteis.analyzeIfFieldIsValid(payment, "codiEmp", None)
            if codiEmp is None:
                codiEmp = self._codiEmp
            historic = funcoesUteis.analyzeIfFieldIsValid(payment, "historic")
            category = funcoesUteis.analyzeIfFieldIsValid(payment, "category")
            accountPlan = funcoesUteis.analyzeIfFieldIsValid(payment, "accountPlan")
            cgcePaying = funcoesUteis.analyzeIfFieldIsValid(payment, "cgcePaying")
            historicExtract = funcoesUteis.analyzeIfFieldIsValid(payment, "historicExtract")
            accountCodeOld = funcoesUteis.analyzeIfFieldIsValid(payment, "accountCodeOld")

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
            sheet.write(row, 23, cgcePaying)
            sheet.write(row, 24, historicExtract)
            sheet.write(row, 25, accountCodeOld)

    def closeFile(self):
        self._workbook.close()
  

# if __name__ == "__main__":
#     generateExcel = GenerateExcel(1428)
#     generateExcel.generateSheetExtract()
