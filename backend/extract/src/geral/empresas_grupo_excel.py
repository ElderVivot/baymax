# coding: utf-8

import os
import sys

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend/extract/src'))
sys.path.append(os.path.join(fileDir, 'backend'))

import pandas as pd
import pyodbc
import json
from datetime import datetime
from dateutil import relativedelta
from dao.src.ConnectMongo import ConnectMongo
from extract.src.geral.geempre import ExtractGeempre
from tools.leArquivos import leXls_Xlsx
import tools.funcoesUteis as funcoesUteis

class extractGeempre():
    def __init__(self):
        self._columns = []
        self._geempre = ExtractGeempre()

        self._connectionMongo = ConnectMongo()
        self._dbMongo = self._connectionMongo.getConnetion()
        self._collection = self._dbMongo['ExtractCompanies']
    
    def process(self):
        try:
            companiesDominio = self._geempre.getCompanies()

            companiesExcel = leXls_Xlsx('C:/Programming/baymax/backend/extract/data/empresas_grupo.xlsm', 'EMPRESAS')

            print('- Exportando dados de movimentação geral empresas:')

            for companie in companiesExcel:
                codi_emp = funcoesUteis.treatNumberField(companie[0], isInt=True)
                nome_emp = funcoesUteis.treatTextField(companie[1])
                group = funcoesUteis.treatTextField(companie[2])

                dataCompanie = {
                    'codi_emp': codi_emp,
                    'groupCompanie': group
                }

                existCompanieDominio = list(filter(lambda companieDominio: companieDominio['codi_emp'] == codi_emp, companiesDominio))
                if len(existCompanieDominio) > 0:
                    self._collection.update_one( { "codi_emp": codi_emp }, { "$set": dataCompanie}, upsert=True )
                    print(f"\t - {codi_emp} - {nome_emp}")

        except Exception as e:
            print(f"O erro é: {e}")
        finally:
            self._connectionMongo.closeConnection()


if __name__ == "__main__":
    geempre = extractGeempre()
    geempre.process()

