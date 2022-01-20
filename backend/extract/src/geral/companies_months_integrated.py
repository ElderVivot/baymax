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
from dateutil.relativedelta import relativedelta
from db.ConexaoBanco import DB
from dao.src.ConnectMongo import ConnectMongo
from tools.leArquivos import readSql
from tools.funcoesUteis import treatTextField, retornaCampoComoData, analyzeIfFieldIsValid
from geempre import ExtractGeempre
import functions.extractFunctions as extractFunctions
# from functions.usefulFunctions import parseTypeFiedValueCorrect

class CompaniesMonthsIntegrated():
    def __init__(self):
        self._DB = DB()
        self._connection = self._DB.getConnection()

        self._connectionMongo = ConnectMongo()
        self._dbMongo = self._connectionMongo.getConnetion()
        self._collection = self._dbMongo['CompaniesMonthsIntegrated'] # vai adicionar na tabela de empresas os dados

    def getCompaniesMonthsIntegrated(self, codiEmp):
        try:
            sql = readSql(os.path.dirname(os.path.abspath(__file__)), 'companies_months_integrated.sql', codiEmp)
            df = pd.read_sql_query(sql, self._connection)
            data = json.loads(df.to_json(orient='records', date_format='iso'))

            return data
        except Exception as e:
            print(e)  

    def checkMonthsIntegrated(self, companieSettingView, companieMonthsIntegrated):
        statusAccountPaid = treatTextField(companieSettingView['statusAccountPaid'])
        isCompanyBranch = treatTextField(companieSettingView['isCompanyBranch'])

        dateAccountPaid = retornaCampoComoData(analyzeIfFieldIsValid(companieSettingView, 'dateAccountPaid', '01/01/1900'))
        dateStart = retornaCampoComoData('01/01/2021')
        dateNow = datetime.today() - relativedelta(months=1)
        
        year = dateStart.year
        startYear = dateStart.year
        startMonth = dateStart.month
        endYear = dateNow.year
        endMonth = dateNow.month

        while year <= endYear:
            months = extractFunctions.returnMonthsOfYear(year, startMonth, startYear, endMonth, endYear)
            
            print('\t\t - ', end='')
            for month in months:
                monthYearFormated = f'{month:0>2}/{year}'
                competence = retornaCampoComoData(f"01/{monthYearFormated}")
                print(f'{monthYearFormated}, ', end='')

                integrated = list(filter(lambda companieMonths: companieMonths['comp'][:10] == f"{year}-{month:0>2}-01", companieMonthsIntegrated))
                
                try:
                    companieSettingView['monthIntegratedMandatory'] = True if dateAccountPaid < competence and \
                        statusAccountPaid.find('CONCLUIDA') >= 0 and statusAccountPaid.find('ANTIGO') < 0 and \
                        isCompanyBranch == "NAO" else False
                except Exception:
                    companieSettingView['monthIntegratedMandatory'] = False

                if len(integrated) > 0:
                    integrated = integrated[0]
                    companieSettingView['existIntegrated'] = True if integrated['qtd_lan_ti_importado_dlan'] > 0 else False
                    
                companieSettingView['qtd_lan_ti_importado_dlan'] = analyzeIfFieldIsValid(integrated, 'qtd_lan_ti_importado_dlan', 0)
                companieSettingView['qtd_lan_ti_importado_dori'] = analyzeIfFieldIsValid(integrated, 'qtd_lan_ti_importado_dori', 0)
                companieSettingView['qtd_lan_operacao'] = analyzeIfFieldIsValid(integrated, 'qtd_lan_operacao', 0)
                companieSettingView['qtd_lan_operacao_dori'] = analyzeIfFieldIsValid(integrated, 'qtd_lan_operacao_dori', 0)
                companieSettingView['cgce_matriz'] = analyzeIfFieldIsValid(integrated, 'cgce_matriz')

                companieSettingView['competence'] = f'{year}-{month:0>2}'
                
                self._collection.update_one( 
                    { 
                        "codi_emp": companieSettingView['codi_emp'],
                        "competence": companieSettingView['competence']
                    }, 
                    { "$set": companieSettingView }, 
                    upsert=True 
                )

            print('')
            year += 1

    def exportData(self):
        print('- Exportando dados de integração:')
        try:
            companiesSettingsView = list(self._dbMongo['CompaniesSettingsView'].find({}))
            for companieSettingView in companiesSettingsView:
                del companieSettingView['_id']

                codiEmp = companieSettingView['codi_emp']
                print(f"\t- Processando empresa {codiEmp} - {companieSettingView['nome_emp']}")

                companieMonthsIntegrated = self.getCompaniesMonthsIntegrated(codiEmp)
                
                self.checkMonthsIntegrated(companieSettingView, companieMonthsIntegrated)

        except Exception as e:
            print(f"Erro ao executar a consulta. O erro é: {e}")
        finally:
            self._connectionMongo.closeConnection()
            self._DB.closeConnection()


if __name__ == "__main__":
    instanceClass = CompaniesMonthsIntegrated()
    instanceClass.exportData()

