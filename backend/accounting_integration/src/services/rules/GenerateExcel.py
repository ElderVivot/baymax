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
            self._workbook = xlsxwriter.Workbook(os.path.join(self._wayBaseToSaveFiles, f"integracao_contabil_{self._codiEmp}_{funcoesUteis.getDateTimeNowInFormatStr()}.xlsx"))
        else:
            self._workbook = xlsxwriter.Workbook(os.path.join(self._wayBaseToSaveFiles, f"atualizado_{nameFileUpdate}"))
        
        self._cell_format_header = self._workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': 'yellow', 'text_wrap': True})
        self._cell_format_header_green = self._workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': 'green', 'text_wrap': True})
        self._cell_format_header_red = self._workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': 'red', 'text_wrap': True})
        self._cell_format_header_orange = self._workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': 'orange', 'text_wrap': True})
        self._cell_format_money = self._workbook.add_format({'num_format': '##0.00'})
        self._cell_format_date = self._workbook.add_format({'num_format': 'dd/mm/yyyy'})
        
    def sheetExtract(self, extracts):
        sheet = self._workbook.add_worksheet('ExtratosBancarios')
        sheet.freeze_panes(1, 0)

        sheet.set_column(9,10,options={'hidden':True})
        sheet.set_column(11,11,options={'hidden':True})
        sheet.set_column(12,12,options={'hidden':True})
        sheet.set_column(14,16,options={'hidden':True})
        sheet.set_column(17,17,options={'hidden':True})

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
        sheet.write(0, 17, "Valor 2", self._cell_format_header)
        sheet.write(0, 18, "Banco/Conta", self._cell_format_header)
        sheet.write(0, 19, "Total Extrato Banco, Dia e Operação", self._cell_format_header_green)
        sheet.write(0, 20, "Total Financeiro + Extrato", self._cell_format_header_orange)
        sheet.write(0, 21, "Diferença", self._cell_format_header_red)
        sheet.write_comment(0, 20, "Esta coluna é o total da aba 'Pagamentos' por banco e dia + o valor do extrato onde a coluna débito e crédito são válidas (diferente de vazio ou zero).")
        sheet.write_comment(0, 21, "Esta coluna é o total do extrato por banco e dia menos o total do financeiro do cliente. Esta coluna sempre deve estar com o valor igual à zero.")

        for key, extract in enumerate(extracts):
            row = key+1
            row2 = key+2

            dateExtract = funcoesUteis.analyzeIfFieldIsValid(extract, "dateTransaction")
            bank = funcoesUteis.analyzeIfFieldIsValid(extract, "bank")
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
            sheet.write_formula(row, 17, f'=IF(AND(B{row2}<>"",B{row2}<>"0",B{row2}<>0,C{row2}<>"",C{row2}<>"0",C{row2}<>0),D{row2},0)', self._cell_format_money)
            sheet.write_formula(row, 18, f'=CONCATENATE(J{row2},"-",K{row2})')
            sheet.write_formula(row, 19, f'=SUMIFS(D:D,A:A,A{row2},S:S,S{row2},N:N,N{row2})', self._cell_format_money)
            sheet.write_formula(row, 20, f'=IF(N{row2}="-",SUMIFS(Pagamentos!O:O,Pagamentos!L:L,ExtratosBancarios!A{row2},Pagamentos!G:G,ExtratosBancarios!S{row2}),0)+SUMIFS(R:R,A:A,A{row2},S:S,S{row2},N:N,N{row2})', self._cell_format_money)
            sheet.write_formula(row, 21, f'=T{row2}-U{row2}', self._cell_format_money)

    def sheetPayments(self, payments):
        sheet = self._workbook.add_worksheet('Pagamentos')
        sheet.freeze_panes(1, 0)

        sheet.set_column(3,3,options={'hidden':True}) # parcela
        sheet.set_column(5,5,options={'hidden':True}) # cnpj fornecedor
        sheet.set_column(8,8,options={'hidden':True}) # comprovante pagto
        sheet.set_column(10,10,options={'hidden':True}) # data extrato
        sheet.set_column(12,12,options={'hidden':True}) # data vencimento
        sheet.set_column(13,13,options={'hidden':True}) # data emissão

        sheet.write(0, 0, "Lote", self._cell_format_header)
        sheet.write(0, 1, "Documento", self._cell_format_header)
        sheet.write(0, 2, "NF na Domínio?", self._cell_format_header)
        sheet.write(0, 3, "Parcela", self._cell_format_header) # hidden
        sheet.write(0, 4, "Fornecedor", self._cell_format_header)
        sheet.write(0, 5, "CNPJ Fornecedor", self._cell_format_header) # hidden
        sheet.write(0, 6, "Banco Financeiro", self._cell_format_header)
        sheet.write(0, 7, "Banco Extrato", self._cell_format_header)
        sheet.write(0, 8, "Comprovante Pagto?", self._cell_format_header)
        sheet.write(0, 9, "Data Financeiro", self._cell_format_header)
        sheet.write(0, 10, "Data Extrato", self._cell_format_header)
        sheet.write(0, 11, "Importação Domínio", self._cell_format_header)
        sheet.write(0, 12, "Vencimento", self._cell_format_header)
        sheet.write(0, 13, "Emissão", self._cell_format_header)
        sheet.write(0, 14, "Valor Pago", self._cell_format_header)
        sheet.write(0, 15, "Desconto", self._cell_format_header)
        sheet.write(0, 16, "Juros", self._cell_format_header)
        sheet.write(0, 17, "Multa", self._cell_format_header)
        sheet.write(0, 18, "Valor Original", self._cell_format_header)
        sheet.write(0, 19, "Conta Contabil Domínio", self._cell_format_header)
        sheet.write(0, 20, "Codigo Empresa", self._cell_format_header)
        sheet.write(0, 21, "Historico Financeiro", self._cell_format_header)
        sheet.write(0, 22, "Categoria", self._cell_format_header)
        sheet.write(0, 23, "Plano de Contas", self._cell_format_header)
        sheet.write(0, 24, "CNPJ Pagador", self._cell_format_header)
        sheet.write(0, 25, "Historico Extrato Bancário", self._cell_format_header)
        sheet.write(0, 26, "Conta Contabil Sistema Cliente", self._cell_format_header)

        # ordena os payments por data
        payments = sorted(payments, key=itemgetter('bank', 'account', 'dateOfImport'))

        for key, payment in enumerate(payments):
            row = key+1

            numberLote = funcoesUteis.analyzeIfFieldIsValid(payment, "numberLote", 0)
            numberLote = row if numberLote == 0 else numberLote
            document = funcoesUteis.analyzeIfFieldIsValid(payment, "document")
            findNote = funcoesUteis.analyzeIfFieldIsValid(payment, "findNote")
            parcelNumber = funcoesUteis.analyzeIfFieldIsValid(payment, "parcelNumber")
            nameProvider = funcoesUteis.analyzeIfFieldIsValid(payment, "nameProvider")
            cgceProvider = funcoesUteis.analyzeIfFieldIsValid(payment, "cgceProvider")
            bankAndAccount = f'{funcoesUteis.analyzeIfFieldIsValid(payment, "bank")}-{funcoesUteis.analyzeIfFieldIsValid(payment, "account")}'
            bankAndAccountExtract = f'{funcoesUteis.analyzeIfFieldIsValid(payment, "bankExtract")}-{funcoesUteis.analyzeIfFieldIsValid(payment, "accountExtract")}'
            foundProof = funcoesUteis.analyzeIfFieldIsValid(payment, "foundProof")
            paymentDate = funcoesUteis.analyzeIfFieldIsValid(payment, "paymentDate", None)
            extractDate = funcoesUteis.analyzeIfFieldIsValid(payment, "dateExtract", None)
            dateOfImport = funcoesUteis.analyzeIfFieldIsValid(payment, "dateOfImport", None)
            dueDate = funcoesUteis.retornaCampoComoData(funcoesUteis.analyzeIfFieldIsValid(payment, "dueDate"))
            issueDate = funcoesUteis.retornaCampoComoData(funcoesUteis.analyzeIfFieldIsValid(payment, "issueDate"))
            amountPaid = funcoesUteis.analyzeIfFieldIsValid(payment, "amountPaid")
            amountDiscount = funcoesUteis.analyzeIfFieldIsValid(payment, "amountDiscount", 0.0)
            amountInterest = funcoesUteis.analyzeIfFieldIsValid(payment, "amountInterest", 0.0)
            amountFine = funcoesUteis.analyzeIfFieldIsValid(payment, "amountFine", 0.0)
            amountOriginal = funcoesUteis.analyzeIfFieldIsValid(payment, "amountOriginal", 0.0)
            accountCode = funcoesUteis.analyzeIfFieldIsValid(payment, "accountCode")
            codiEmp = funcoesUteis.analyzeIfFieldIsValid(payment, "companyBranch", None)
            codiEmp = self._codiEmp if codiEmp is None or str(codiEmp).isnumeric() is False else codiEmp
            historic = funcoesUteis.analyzeIfFieldIsValid(payment, "historic")
            category = funcoesUteis.analyzeIfFieldIsValid(payment, "category")
            accountPlan = funcoesUteis.analyzeIfFieldIsValid(payment, "accountPlan")
            cgcePaying = funcoesUteis.analyzeIfFieldIsValid(payment, "cgcePaying")
            historicExtract = funcoesUteis.analyzeIfFieldIsValid(payment, "historicExtract")
            accountCodeOld = funcoesUteis.analyzeIfFieldIsValid(payment, "accountCodeOld")

            sheet.write(row, 0, numberLote)
            sheet.write(row, 1, document)
            sheet.write(row, 2, findNote)
            sheet.write(row, 3, parcelNumber)
            sheet.write(row, 4, nameProvider)
            sheet.write(row, 5, cgceProvider)
            sheet.write(row, 6, bankAndAccount)
            sheet.write(row, 7, bankAndAccountExtract)
            sheet.write(row, 8, foundProof)
            sheet.write(row, 9, paymentDate, self._cell_format_date)
            sheet.write(row, 10, extractDate, self._cell_format_date)
            sheet.write(row, 11, dateOfImport, self._cell_format_date)
            sheet.write(row, 12, dueDate, self._cell_format_date)
            sheet.write(row, 13, issueDate, self._cell_format_date)
            sheet.write(row, 14, amountPaid, self._cell_format_money)
            sheet.write(row, 15, amountDiscount, self._cell_format_money)
            sheet.write(row, 16, amountInterest, self._cell_format_money)
            sheet.write(row, 17, amountFine, self._cell_format_money)
            sheet.write(row, 18, amountOriginal, self._cell_format_money)
            sheet.write(row, 19, accountCode)
            sheet.write(row, 20, codiEmp)
            sheet.write(row, 21, historic)
            sheet.write(row, 22, category)
            sheet.write(row, 23, accountPlan)
            sheet.write(row, 24, cgcePaying)
            sheet.write(row, 25, historicExtract)
            sheet.write(row, 26, accountCodeOld)

    def closeFile(self):
        self._workbook.close()
  

# if __name__ == "__main__":
#     generateExcel = GenerateExcel(1428)
#     generateExcel.generateSheetExtract()
