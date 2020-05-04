# coding: utf-8

import os
import sys

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend/extract/src'))
sys.path.append(os.path.join(fileDir, 'backend'))

import json
import datetime
from dao.src.ConnectMongo import ConnectMongo
from extract.src.geral.geempre import ExtractGeempre
from tools.leArquivos import readJson, readSql, leXls_Xlsx
import tools.funcoesUteis as funcoesUteis
import functions.extractFunctions as extractFunctions

class AnalyzesFixedAssetsProducts(object):
    def __init__(self):
        self._namesProductsBase = leXls_Xlsx(os.path.join('C:/Programming/baymax/backend/extract/data/bkp', 'produtos_comparar.xlsx'))
        self._namesProductsBase = funcoesUteis.removeAnArrayFromWithinAnother(self._namesProductsBase)
        self._geempre = ExtractGeempre()
        self._today = datetime.date.today()
        self._currentMonth = self._today.month
        self._currentYear = self._today.year

        self._connectionMongo = ConnectMongo()
        self._dbMongo = self._connectionMongo.getConnetion()
        self._collection = self._dbMongo['ExtractEntryNoteProducts']

    def getProductsFixedAssets(self, codi_emp, month, year, products):
        try:
            collectionFixedAssets = self._dbMongo['EntryNoteProductsFixedAssets']
            collectionFixedAssets.delete_many( {"$and": [{'codi_emp': codi_emp}, {'monthFilter': month}, {'yearFilter': year}] } )

            for product in products:
                if str(product['cfop']) in ('1551', '2551', '3551', '1406', '2406'):
                    product['classificado_corretamente_cfop'] = True
                    collectionFixedAssets.insert_one(product)
                elif str(product['cfop']) in ('1556', '2556', '3556', '1407', '2407'):
                    vunit = funcoesUteis.treatDecimalField(product['vunit'])
                    if vunit >= 1200:
                        desc_pdi = funcoesUteis.treatTextField(product['desc_pdi'])
                        hasNameProductFixedAsset = list(filter(lambda name: desc_pdi.find(funcoesUteis.treatTextField(name)) >= 0, self._namesProductsBase))
                        if len(hasNameProductFixedAsset) > 0:
                            product['classificado_corretamente_cfop'] = False
                            collectionFixedAssets.insert_one(product)
                        else:
                            continue
                else:
                    continue
        except Exception:
            pass

    def process(self, filterCompanie=0, filterMonthStart=5, filterYearStart=2015, filterMonthEnd=0, filterYearEnd=0):
        filterMonthEnd = self._currentMonth if filterMonthEnd == 0 else filterMonthEnd
        filterYearEnd = self._currentYear if filterYearEnd == 0 else filterYearEnd

        try:
            companies = self._geempre.getCompanies()

            for companie in companies:
                codi_emp = companie['codi_emp']

                if filterCompanie != 0 and filterCompanie != codi_emp:
                    continue # ignora as empresas que não estão no filtro

                print(f"- Procurando produtos imobilizados {codi_emp} - {companie['nome_emp']}")
                
                competenceStartEnd = extractFunctions.returnCompetenceStartEnd(companie, filterMonthStart, filterYearStart, filterMonthEnd, filterYearEnd)
                startMonth = competenceStartEnd['filterMonthStart']
                startYear = competenceStartEnd['filterYearStart']
                endMonth = competenceStartEnd['filterMonthEnd']
                endYear = competenceStartEnd['filterYearEnd']

                year = startYear

                while year <= endYear:

                    months = extractFunctions.returnMonthsOfYear(year, startMonth, startYear, endMonth, endYear)

                    print('\t - ', end='')
                    for month in months:
                        print(f'{month:0>2}/{year}, ', end='')

                        products = self._collection.find({"$and": [{'codi_emp': codi_emp}, {'monthFilter': month}, {'yearFilter': year}] })
                        self.getProductsFixedAssets(codi_emp, month, year, products)

                    print('')
                    year += 1
        except Exception as e:
            print(f"Erro: {e}")
        finally:
            self._connectionMongo.closeConnection()

if __name__ == "__main__":
    obj = AnalyzesFixedAssetsProducts()
    obj.process()