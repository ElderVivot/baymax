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

    def __init__(self, codiEmp, lancamentos):
        self._codiEmp = codiEmp
        self._lancamentos = lancamentos

        self._wayBaseToSaveFiles = os.path.join(wayDefault['WayToSaveFilesOriginals'], f'{self._codiEmp}/arquivos_processados')
        
        if os.path.exists(self._wayBaseToSaveFiles) is False:
            os.makedirs(self._wayBaseToSaveFiles)

        self._workbook = xlsxwriter.Workbook(os.path.join(self._wayBaseToSaveFiles, f"folha_pagto_{self._codiEmp}_{funcoesUteis.getDateTimeNowInFormatStr()}.xlsx"))
        
        self._cell_format_header = self._workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': 'yellow', 'text_wrap': True})
        self._cell_format_money = self._workbook.add_format({'num_format': '##0.00'})
        self._cell_format_date = self._workbook.add_format({'num_format': 'dd/mm/yyyy'})
        
    def sheetFolhaPagto(self):
        sheet = self._workbook.add_worksheet('Lancamentos')
        
        sheet.freeze_panes(1, 0)

        sheet.write(0, 0, "Data", self._cell_format_header)
        sheet.write(0, 1, "Empresa", self._cell_format_header)
        sheet.write(0, 2, "Cod. Rubrica", self._cell_format_header)
        sheet.write(0, 3, "Nome Rubrica", self._cell_format_header)
        sheet.write(0, 4, "Valor", self._cell_format_header)
        sheet.write(0, 5, "Provento / Desconto", self._cell_format_header)
        sheet.write(0, 6, "Tipo Colaborador", self._cell_format_header)
        sheet.write(0, 7, "Cod. Debito", self._cell_format_header)
        sheet.write(0, 8, "Cod. Credito", self._cell_format_header)
        
        for key, lancamento in enumerate(self._lancamentos):
            row = key+1

            dateLanc = funcoesUteis.analyzeIfFieldIsValid(lancamento, "dateLanc")
            nameCompany = funcoesUteis.analyzeIfFieldIsValid(lancamento, "nameCompany")
            codeRubrica = funcoesUteis.analyzeIfFieldIsValid(lancamento, "codeRubrica")
            nameRubrica = funcoesUteis.analyzeIfFieldIsValid(lancamento, "nameRubrica")
            amountRubrica = funcoesUteis.analyzeIfFieldIsValid(lancamento, "amountRubrica")
            typeColaborador = funcoesUteis.analyzeIfFieldIsValid(lancamento, "typeColaborador")
            typeEvent = funcoesUteis.analyzeIfFieldIsValid(lancamento, "typeEvent")
            
            sheet.write(row, 0, dateLanc, self._cell_format_date)
            sheet.write(row, 1, nameCompany)
            sheet.write(row, 2, codeRubrica)
            sheet.write(row, 3, nameRubrica)
            sheet.write(row, 4, amountRubrica, self._cell_format_money)
            sheet.write(row, 5, typeEvent)
            sheet.write(row, 6, typeColaborador)
            
    def closeFile(self):
        self._workbook.close()
  

# if __name__ == "__main__":
#     generateExcel = GenerateExcel(1428)
#     generateExcel.generateSheetExtract()
