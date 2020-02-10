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

        self._workbook = xlsxwriter.Workbook(os.path.join(self._wayBaseToSaveFiles, f"livro_caixa_{self._codiEmp}_{funcoesUteis.getDateTimeNowInFormatStr()}.xlsx"))
        
        self._cell_format_header = self._workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': 'yellow', 'text_wrap': True})
        self._cell_format_money = self._workbook.add_format({'num_format': '##0.00'})
        self._cell_format_date = self._workbook.add_format({'num_format': 'dd/mm/yyyy'})
        
    def sheetLivroCaixa(self, livrosCaixas):
        sheet = self._workbook.add_worksheet('Lancamentos')
        
        sheet.freeze_panes(1, 0)

        sheet.write(0, 0, "Data", self._cell_format_header)
        sheet.write(0, 1, "Tipo Movimento", self._cell_format_header)
        sheet.write(0, 2, "Conta Contábil", self._cell_format_header)
        sheet.write(0, 3, "Nome Conta", self._cell_format_header)
        sheet.write(0, 4, "Valor", self._cell_format_header)
        sheet.write(0, 5, "Documento", self._cell_format_header)
        sheet.write(0, 6, "Tipo Documento", self._cell_format_header)
        sheet.write(0, 7, "Participante", self._cell_format_header)
        sheet.write(0, 8, "Imóvel Rural", self._cell_format_header)
        sheet.write(0, 9, "Histórico", self._cell_format_header)
        
        for key, livroCaixa in enumerate(livrosCaixas):
            row = key+1

            dateLivro = funcoesUteis.analyzeIfFieldIsValid(livroCaixa, "dateLivro")
            movementType = funcoesUteis.analyzeIfFieldIsValid(livroCaixa, "movementType")
            account = funcoesUteis.analyzeIfFieldIsValid(livroCaixa, "account")
            nameAccount = funcoesUteis.analyzeIfFieldIsValid(livroCaixa, "nameAccount")
            amount = funcoesUteis.analyzeIfFieldIsValid(livroCaixa, "amount")
            document = funcoesUteis.analyzeIfFieldIsValid(livroCaixa, "document")
            documentType = funcoesUteis.analyzeIfFieldIsValid(livroCaixa, "documentType")
            participante = 1
            imovelRural = 1
            historic = funcoesUteis.analyzeIfFieldIsValid(livroCaixa, "historic")
            
            sheet.write(row, 0, dateLivro, self._cell_format_date)
            sheet.write(row, 1, movementType)
            sheet.write(row, 2, account)
            sheet.write(row, 3, nameAccount)
            sheet.write(row, 4, amount, self._cell_format_money)
            sheet.write(row, 5, document)
            sheet.data_validation(f'G{row+1}', {'validate': 'list', 'source': ['Nota Fiscal', 'Fatura', 'Recibo', 'Contrato', 'Folha de Pagamento', 'Outros']})
            sheet.write(row, 7, participante)
            sheet.write(row, 8, imovelRural)
            sheet.write(row, 9, historic)

    def sheetAccountPlan(self, accountPlan):
        sheet = self._workbook.add_worksheet('PlanoContas')
        row = 1

        sheet.freeze_panes(1, 0)

        sheet.write(0, 0, "Conta", self._cell_format_header)
        sheet.write(0, 1, "Nome", self._cell_format_header)
        sheet.write(0, 2, "Grupo Principal", self._cell_format_header)
        sheet.write(0, 3, "Subgrupo", self._cell_format_header)
        sheet.write(0, 4, "Código Conta Domínio", self._cell_format_header)

        for key, livroCaixa in accountPlan.items():
            account = key
            nameAccount = livroCaixa[0]
            nameAccountMain = livroCaixa[1]
            nameAccountSubMain = livroCaixa[2]

            sheet.write(row, 0, account)
            sheet.write(row, 1, nameAccount)
            sheet.write(row, 2, nameAccountMain)
            sheet.write(row, 3, nameAccountSubMain)
            sheet.write(row, 4, '')

            row += 1
            
    def closeFile(self):
        self._workbook.close()
  

# if __name__ == "__main__":
#     generateExcel = GenerateExcel(1428)
#     generateExcel.generateSheetExtract()
