import sys
import os

fileDir = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(fileDir)
print(sys.path)

import os
import json
from tools.leArquivos import leXls_Xlsx

# 1556, 2556, 1407 e 2407

class AnalisaNotasImobilizado(object):
    def __init__(self):
        self._wayCompanies = os.path.join(fileDir, 'extract/data/empresas.json')
        self._wayEntryNotes = os.path.join(fileDir, 'extract/data/entradas')
        self._namesProductsBase =  leXls_Xlsx(os.path.join(fileDir, 'extract/data/produtos_comparar.xlsx'))
        print(self._namesProductsBase)

    # def noteIsAnAsset(self, notesProducts):
    #     with open(self.notesProducts) as products:
    #         data = json.load(products)
    #         for product in products:
    #             if product['cfop_mep'] in ('1556', '2556', '1407', '2407'):
                    

    # def processIfNoteIsAnAsset(self, filterCompanie=0):
    #     with open(self._wayCompanies) as companies:
    #         data = json.load(companies)
    #         for companie in data:
    #             if companie['stat_emp'] not in ('I') and companie['dina_emp'] is None:
    #                     if companie['codi_emp'] == filterCompanie or filterCompanie == 0:
    #                         self._wayEntryNotesProducts = os.path.join(fileDir, f"extract/data/entradas_produtos/{companie['codi_emp']}-efmvepro.json")
                            
