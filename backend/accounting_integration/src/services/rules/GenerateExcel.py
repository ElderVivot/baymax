import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import xlsxwriter
import tools.funcoesUteis as funcoesUteis


class GenerateExcel(object):

    def __init__(self, codiEmp):
        self._codiEmp = codiEmp
        self._workbook = xlsxwriter.Workbook(f'C:/integracao_contabil/{self._codiEmp}/contas_pagas.xlsx')
        self._cell_format_header = self._workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': 'yellow'})
        self._cell_format_money = self._workbook.add_format({'num_format': '##0.00'})
        
    def generateSheetExtract(self, extracts):
        # extracts = [{'bankId': 'CEF', 'account': '000514930', 'typeTransaction': 'CREDIT', 'dateTransaction': '30/10/2019', 'amount': 605.0, 'operation': '+', 'document': '301502', 'historic': 'DP DIN LOT'}, {'bankId': 'CEF', 'account': '000514930', 'typeTransaction': 'CREDIT', 'dateTransaction': '31/10/2019', 'amount': 87.0, 'operation': '+', 'document': '311415', 'historic': 'DP DIN LOT'}]
        
        sheet1 = self._workbook.add_worksheet('ExtratosBancarios')

        sheet1.write(0, 0, "Data", self._cell_format_header)
        sheet1.write(0, 1, "Debito", self._cell_format_header)
        sheet1.write(0, 2, "Credito", self._cell_format_header)
        sheet1.write(0, 3, "Valor", self._cell_format_header)
        sheet1.write(0, 4, "Cod. Hist", self._cell_format_header)
        sheet1.write(0, 5, "Historico", self._cell_format_header)
        sheet1.write(0, 6, "-------", self._cell_format_header)
        sheet1.write(0, 7, "-------", self._cell_format_header)
        sheet1.write(0, 8, "Banco", self._cell_format_header)
        sheet1.write(0, 9, "Conta Corrente", self._cell_format_header)
        sheet1.write(0, 10, "Data Extrato", self._cell_format_header)
        sheet1.write(0, 11, "Tipo Transacao", self._cell_format_header)
        sheet1.write(0, 12, "Operacao", self._cell_format_header)
        sheet1.write(0, 13, "Valor", self._cell_format_header)
        sheet1.write(0, 14, "Documento", self._cell_format_header)
        sheet1.write(0, 15, "Historico", self._cell_format_header)

        for key, extract in enumerate(extracts):
            row = key+1

            dateExtract = funcoesUteis.analyzeIfFieldIsValid(extract, "dateTransaction")
            bank = funcoesUteis.analyzeIfFieldIsValid(extract, "bankId")
            account = funcoesUteis.analyzeIfFieldIsValid(extract, "account")
            typeTransaction = funcoesUteis.analyzeIfFieldIsValid(extract, "typeTransaction")
            operation = funcoesUteis.analyzeIfFieldIsValid(extract, "operation")
            document = funcoesUteis.analyzeIfFieldIsValid(extract, "document")
            historic = funcoesUteis.analyzeIfFieldIsValid(extract, "historic")
            amount = funcoesUteis.analyzeIfFieldIsValid(extract, "amount")

            sheet1.write(row, 0, dateExtract)
            sheet1.write(row, 1, "")
            sheet1.write(row, 2, "")
            sheet1.write(row, 3, amount, self._cell_format_money)
            sheet1.write(row, 4, "")
            sheet1.write(row, 5, historic)
            sheet1.write(row, 6, "")
            sheet1.write(row, 7, "")
            sheet1.write(row, 8, bank)
            sheet1.write(row, 9, account)
            sheet1.write(row, 10, dateExtract)
            sheet1.write(row, 11, typeTransaction)
            sheet1.write(row, 12, operation)
            sheet1.write(row, 13, amount, self._cell_format_money)
            sheet1.write(row, 14, document)
            sheet1.write(row, 15, historic)

        self._workbook.close()

    def generateSheetPayments(self, payments):
        # extracts = [{'bankId': 'CEF', 'account': '000514930', 'typeTransaction': 'CREDIT', 'dateTransaction': '30/10/2019', 'amount': 605.0, 'operation': '+', 'document': '301502', 'historic': 'DP DIN LOT'}, {'bankId': 'CEF', 'account': '000514930', 'typeTransaction': 'CREDIT', 'dateTransaction': '31/10/2019', 'amount': 87.0, 'operation': '+', 'document': '311415', 'historic': 'DP DIN LOT'}]
        
        sheet1 = self._workbook.add_worksheet('Pagamentos')

        sheet1.write(0, 0, "Documento", self._cell_format_header)
        sheet1.write(0, 1, "Encontrou a NF na Domínio?", self._cell_format_header)
        sheet1.write(0, 2, "Nome Fornecedor", self._cell_format_header)
        sheet1.write(0, 3, "CNPJ Fornecedor", self._cell_format_header)
        sheet1.write(0, 4, "Banco Planilha Cliente", self._cell_format_header)
        sheet1.write(0, 5, "Banco Extrato", self._cell_format_header)
        sheet1.write(0, 6, "Encontrou Comprovante Pagto?", self._cell_format_header)
        sheet1.write(0, 7, "Data de Pagto", self._cell_format_header)
        sheet1.write(0, 8, "Data do Extrato", self._cell_format_header)
        sheet1.write(0, 9, "Data do Lançamento na Domínio", self._cell_format_header)
        sheet1.write(0, 10, "Data do Vencimento", self._cell_format_header)
        sheet1.write(0, 11, "Data do Emissão", self._cell_format_header)
        sheet1.write(0, 12, "Valor Pago", self._cell_format_header)
        sheet1.write(0, 13, "Valor Desconto", self._cell_format_header)
        sheet1.write(0, 14, "Valor Juros", self._cell_format_header)
        sheet1.write(0, 15, "Valor Multa", self._cell_format_header)
        sheet1.write(0, 16, "Valor Original", self._cell_format_header)
        sheet1.write(0, 17, "Conta Contabil Domínio", self._cell_format_header)
        sheet1.write(0, 18, "Codigo Empresa", self._cell_format_header)
        sheet1.write(0, 19, "Historico Planilha", self._cell_format_header)
        sheet1.write(0, 20, "Categoria", self._cell_format_header)
        sheet1.write(0, 21, "Plano de Contas", self._cell_format_header)
        sheet1.write(0, 22, "Tipo de Pagamento", self._cell_format_header)
        sheet1.write(0, 23, "Historico Extrato Bancário", self._cell_format_header)

        for key, payment in enumerate(payments):
            row = key+1

            document = funcoesUteis.analyzeIfFieldIsValid(payment, "document")
            findNote = funcoesUteis.analyzeIfFieldIsValid(payment, "findNote")
            nameProvider = funcoesUteis.analyzeIfFieldIsValid(payment, "nameProvider")
            cgceProvider = funcoesUteis.analyzeIfFieldIsValid(payment, "cgceProvider")
            bankAndAccount = f'{funcoesUteis.analyzeIfFieldIsValid(payment, "bank")}-{funcoesUteis.analyzeIfFieldIsValid(payment, "account")}'
            bankAndAccountExtract = f'{funcoesUteis.analyzeIfFieldIsValid(payment, "bankExtract")}-{funcoesUteis.analyzeIfFieldIsValid(payment, "accountExtract")}'
            foundProof = funcoesUteis.analyzeIfFieldIsValid(payment, "foundProof")
            paymentDate = funcoesUteis.analyzeIfFieldIsValid(payment, "paymentDate", None)
            extractDate = funcoesUteis.analyzeIfFieldIsValid(payment, "dateExtract", None)
            if extractDate is None:
                dateOfImport = paymentDate
            else:
                dateOfImport = extractDate
            dueDate = funcoesUteis.analyzeIfFieldIsValid(payment, "dueDate")
            issueDate = funcoesUteis.analyzeIfFieldIsValid(payment, "issueDate")
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

            sheet1.write(row, 0, document)
            sheet1.write(row, 1, findNote)
            sheet1.write(row, 2, nameProvider)
            sheet1.write(row, 3, cgceProvider)
            sheet1.write(row, 4, bankAndAccount)
            sheet1.write(row, 5, bankAndAccountExtract)
            sheet1.write(row, 6, foundProof)
            sheet1.write(row, 7, paymentDate)
            sheet1.write(row, 8, extractDate)
            sheet1.write(row, 9, dueDate)
            sheet1.write(row, 10, dueDate)
            sheet1.write(row, 11, issueDate)
            sheet1.write(row, 12, amountPaid, self._cell_format_money)
            sheet1.write(row, 13, amountDiscount, self._cell_format_money)
            sheet1.write(row, 14, amountInterest, self._cell_format_money)
            sheet1.write(row, 15, amountFine, self._cell_format_money)
            sheet1.write(row, 16, amountOriginal, self._cell_format_money)
            sheet1.write(row, 17, accountCode)
            sheet1.write(row, 18, codiEmp)
            sheet1.write(row, 19, historic)
            sheet1.write(row, 20, category)
            sheet1.write(row, 21, accountPlan)
            sheet1.write(row, 22, paymentType)
            sheet1.write(row, 23, historicExtract)

    def closeFile(self):
        self._workbook.close()
  

# if __name__ == "__main__":
#     generateExcel = GenerateExcel(1428)
#     generateExcel.generateSheetExtract()
