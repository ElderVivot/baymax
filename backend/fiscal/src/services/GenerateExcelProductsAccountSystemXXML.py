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
from pymongo import MongoClient

wayToSaveFiles = open(os.path.join(fileDir, 'backend/accounting_integration/src/WayToSaveFiles.json') )
wayDefault = json.load(wayToSaveFiles)
wayToSaveFiles.close()


class GenerateExcelProductsAccountSystemXXML(object):

    def __init__(self, wayToSaveFile):
        self._wayToSaveFile = wayToSaveFile
        self._workbook = xlsxwriter.Workbook(os.path.join(self._wayToSaveFile, f"produtos_comparacao.xlsx"))
        self._cell_format_header = self._workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': 'yellow', 'text_wrap': True})
        self._cell_format_money = self._workbook.add_format({'num_format': '##0.00'})
        self._cell_format_date = self._workbook.add_format({'num_format': 'dd/mm/yyyy'})

        self._client = MongoClient() # conecta num cliente do MongoDB rodando na sua máquina
        self._db = self._client.baymax
        self._collection = self._db[f'ProductComparationBetweenAccountSystemAndXML']
    
    def sheetProducts(self):
        sheet = self._workbook.add_worksheet('Products')
        sheet.freeze_panes(1, 0)

        sheet.set_column(9,11,options={'hidden':True}) # qtd, valor unitário e valor total domínio
        sheet.set_column(14,16,options={'hidden':True}) # qtd, valor unitário e valor total xml

        sheet.write(0, 0, "Código Empresa", self._cell_format_header)
        sheet.write(0, 1, "Código Nota", self._cell_format_header)
        sheet.write(0, 2, "Número", self._cell_format_header)
        sheet.write(0, 3, "Cliente/Fornecedor", self._cell_format_header)
        sheet.write(0, 4, "Emissão", self._cell_format_header)
        sheet.write(0, 5, "Entrada/Saída", self._cell_format_header)
        sheet.write(0, 6, "Código Produto Domínio", self._cell_format_header)
        sheet.write(0, 7, "Descrição", self._cell_format_header)
        sheet.write(0, 8, "CFOP", self._cell_format_header)
        sheet.write(0, 9, "Quantidade", self._cell_format_header)
        sheet.write(0, 10, "Valor Unitário", self._cell_format_header)
        sheet.write(0, 11, "Valor Total", self._cell_format_header)
        sheet.write(0, 12, "Código Produto XML", self._cell_format_header)
        sheet.write(0, 13, "Descrição", self._cell_format_header)
        sheet.write(0, 14, "Quantidade", self._cell_format_header)
        sheet.write(0, 15, "Valor Unitário", self._cell_format_header)
        sheet.write(0, 16, "Valor Total", self._cell_format_header)
        sheet.write(0, 17, "Comparação", self._cell_format_header)
        sheet.write(0, 18, "Chave Nota", self._cell_format_header)

        productsAccountSystemXXML = self._collection.find()

        for key, productAccountSystemXXML in enumerate(productsAccountSystemXXML):
            row = key+1

            codiEmp = funcoesUteis.analyzeIfFieldIsValid(productAccountSystemXXML, "codiEmp")
            print(codiEmp)

    def closeFile(self):
        self._workbook.close()
  

if __name__ == "__main__":
    generateExcelProductsAccountSystemXXML = GenerateExcelProductsAccountSystemXXML('C:/_temp')
    generateExcelProductsAccountSystemXXML.sheetProducts()
