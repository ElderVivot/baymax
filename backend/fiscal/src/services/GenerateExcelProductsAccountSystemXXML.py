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

        sheet.set_column(10,12,options={'hidden':True}) # qtd, valor unitário e valor total domínio
        sheet.set_column(15,17,options={'hidden':True}) # qtd, valor unitário e valor total xml

        sheet.write(0, 0, "Código Empresa", self._cell_format_header)
        sheet.write(0, 1, "Código Nota", self._cell_format_header)
        sheet.write(0, 2, "Número", self._cell_format_header)
        sheet.write(0, 3, "Tipo Nota", self._cell_format_header)
        sheet.write(0, 4, "Cliente/Fornecedor", self._cell_format_header)
        sheet.write(0, 5, "Emissão", self._cell_format_header)
        sheet.write(0, 6, "Entrada/Saída", self._cell_format_header)
        sheet.write(0, 7, "Código Produto Domínio", self._cell_format_header)
        sheet.write(0, 8, "Descrição", self._cell_format_header)
        sheet.write(0, 9, "CFOP", self._cell_format_header)
        sheet.write(0, 10, "Quantidade", self._cell_format_header)
        sheet.write(0, 11, "Valor Unitário", self._cell_format_header)
        sheet.write(0, 12, "Valor Total", self._cell_format_header)
        sheet.write(0, 13, "Código Produto XML", self._cell_format_header)
        sheet.write(0, 14, "Descrição", self._cell_format_header)
        sheet.write(0, 15, "Quantidade", self._cell_format_header)
        sheet.write(0, 16, "Valor Unitário", self._cell_format_header)
        sheet.write(0, 17, "Valor Total", self._cell_format_header)
        sheet.write(0, 18, "Comparação", self._cell_format_header)
        sheet.write(0, 19, "Chave Nota", self._cell_format_header)

        productsAccountSystemXXML = self._collection.find()        

        for key, productAccountSystemXXML in enumerate(productsAccountSystemXXML):
            row = key+1
            
            print(f' - Processando {row}')
            
            codiEmp = funcoesUteis.analyzeIfFieldIsValid(productAccountSystemXXML, "codiEmp")
            codiNote = funcoesUteis.returnDataFieldInDict(productAccountSystemXXML, ["productDominio", "codigo_nota"])
            numberNote = funcoesUteis.returnDataFieldInDict(productAccountSystemXXML, ["productDominio", "numero"])
            typeNF = funcoesUteis.analyzeIfFieldIsValid(productAccountSystemXXML, "typeNF")
            cliFor = funcoesUteis.returnDataFieldInDict(productAccountSystemXXML, ["productDominio", "cli_for"])
            issueDate = funcoesUteis.retornaCampoComoData(funcoesUteis.returnDataFieldInDict(productAccountSystemXXML, ["productDominio", "emissao"]),2)
            saidaEntradaDate = funcoesUteis.retornaCampoComoData(funcoesUteis.returnDataFieldInDict(productAccountSystemXXML, ["productDominio", "saida_entrada"]),2)
            codeProductAccountSystem = funcoesUteis.returnDataFieldInDict(productAccountSystemXXML, ["productDominio", "codi_pdi"]).strip()
            nameProductAccountSystem = funcoesUteis.treatTextField(funcoesUteis.returnDataFieldInDict(productAccountSystemXXML, ["productDominio", "desc_pdi"]))
            cfopProductAccountSystem = funcoesUteis.returnDataFieldInDict(productAccountSystemXXML, ["productDominio", "cfop"])
            qtdProductAccountSystem = funcoesUteis.treatDecimalField(funcoesUteis.returnDataFieldInDict(productAccountSystemXXML, ["productDominio", "qtd"]))
            vunitProductAccountSystem = funcoesUteis.treatDecimalField(funcoesUteis.returnDataFieldInDict(productAccountSystemXXML, ["productDominio", "vunit"]))
            vtotProductAccountSystem = funcoesUteis.treatDecimalField(funcoesUteis.returnDataFieldInDict(productAccountSystemXXML, ["productDominio", "vtot"]))
            codeProductXML = funcoesUteis.returnDataFieldInDict(productAccountSystemXXML, ["productXML", "prod", "cProd"]).strip()
            nameProductXML = funcoesUteis.treatTextField(funcoesUteis.returnDataFieldInDict(productAccountSystemXXML, ["productXML", "prod", "xProd"]))
            qtdProductXML= funcoesUteis.treatDecimalField(funcoesUteis.returnDataFieldInDict(productAccountSystemXXML, ["productXML", "prod", "qCom"]))
            vunitProductXML = funcoesUteis.treatDecimalField(funcoesUteis.returnDataFieldInDict(productAccountSystemXXML, ["productXML", "prod", "vUnCom"]))
            vtotProductXML = funcoesUteis.treatDecimalField(funcoesUteis.returnDataFieldInDict(productAccountSystemXXML, ["productXML", "prod", "vProd"]))
            valueComparationBetweenAccountSystemAndXML = funcoesUteis.treatDecimalField(funcoesUteis.returnDataFieldInDict(productAccountSystemXXML, ["valueComparationBetweenAccountSystemAndXML"]))
            keyNF = funcoesUteis.returnDataFieldInDict(productAccountSystemXXML, ["productDominio", "chave_nfe"])

            sheet.write(row, 0, codiEmp)
            sheet.write(row, 1, codiNote)
            sheet.write(row, 2, numberNote)
            sheet.write(row, 3, typeNF)
            sheet.write(row, 4, cliFor)
            sheet.write(row, 5, issueDate, self._cell_format_date)
            sheet.write(row, 6, saidaEntradaDate, self._cell_format_date)
            sheet.write(row, 7, codeProductAccountSystem)
            sheet.write(row, 8, nameProductAccountSystem)
            sheet.write(row, 9, cfopProductAccountSystem)
            sheet.write(row, 10, qtdProductAccountSystem, self._cell_format_money)
            sheet.write(row, 11, vunitProductAccountSystem, self._cell_format_money)
            sheet.write(row, 12, vtotProductAccountSystem, self._cell_format_money)
            sheet.write(row, 13, codeProductXML)
            sheet.write(row, 14, nameProductXML)
            sheet.write(row, 15, qtdProductXML, self._cell_format_money)
            sheet.write(row, 16, vunitProductXML, self._cell_format_money)
            sheet.write(row, 17, vtotProductXML, self._cell_format_money)
            sheet.write(row, 18, valueComparationBetweenAccountSystemAndXML, self._cell_format_money)
            sheet.write(row, 19, keyNF)

    def closeFile(self):
        self._workbook.close()
  

if __name__ == "__main__":
    generateExcelProductsAccountSystemXXML = GenerateExcelProductsAccountSystemXXML('C:/_temp')
    generateExcelProductsAccountSystemXXML.sheetProducts()
    generateExcelProductsAccountSystemXXML.closeFile()
