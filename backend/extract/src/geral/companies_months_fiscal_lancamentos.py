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
from tools.funcoesUteis import treatTextField, retornaCampoComoData, analyzeIfFieldIsValid, analyzeIfFieldIsValidMatrix, treatNumberField
from geempre import ExtractGeempre
import functions.extractFunctions as extractFunctions
# from functions.usefulFunctions import parseTypeFiedValueCorrect

class CompaniesMonthsIntegrated():
    def __init__(self):
        self._DB = DB()
        self._connection = self._DB.getConnection()

        self._connectionMongo = ConnectMongo()
        self._dbMongo = self._connectionMongo.getConnetion()
        self._collection = self._dbMongo['CompaniesMonthsAmountNotes']

    def getCompaniesMonthsAmountNotes(self, cgceMatriz):
        try:
            sql = readSql(os.path.dirname(os.path.abspath(__file__)), 'companies_months_fiscal_lancamentos.sql', cgceMatriz, cgceMatriz, cgceMatriz)
            df = pd.read_sql_query(sql, self._connection)
            data = json.loads(df.to_json(orient='records', date_format='iso'))

            return data
        except Exception as e:
            print(e)  

    def saveMongo(self, codiEmp, cgceMatriz, companieMonthsAmountNotes):
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
                companieDataToSave = {}

                monthYearFormated = f'{month:0>2}/{year}'
                print(f'{monthYearFormated}, ', end='')

                amountNotaSaida = list(filter(lambda companieMonths: companieMonths['comp'][:10] == f"{year}-{month:0>2}-01" \
                    and companieMonths['tipo'] == 'SAIDA', companieMonthsAmountNotes))
                amountNotaSaida = analyzeIfFieldIsValidMatrix(amountNotaSaida, 1, [])

                amountNotaEntrada = list(filter(lambda companieMonths: companieMonths['comp'][:10] == f"{year}-{month:0>2}-01" \
                    and companieMonths['tipo'] == 'ENTRADA', companieMonthsAmountNotes))
                amountNotaEntrada = analyzeIfFieldIsValidMatrix(amountNotaEntrada, 1, [])

                amountNotaServico = list(filter(lambda companieMonths: companieMonths['comp'][:10] == f"{year}-{month:0>2}-01" \
                    and companieMonths['tipo'] == 'SERVICO', companieMonthsAmountNotes))
                amountNotaServico = analyzeIfFieldIsValidMatrix(amountNotaServico, 1, [])
    
                companieDataToSave['qtd_notas_saidas_operacao'] = analyzeIfFieldIsValid(amountNotaSaida, 'qtd_notas_operacao', 0)
                companieDataToSave['qtd_notas_saidas_operacao_dori'] = analyzeIfFieldIsValid(amountNotaSaida, 'qtd_notas_operacao_dori', 0)
                companieDataToSave['qtd_notas_entradas_operacao'] = analyzeIfFieldIsValid(amountNotaEntrada, 'qtd_notas_operacao', 0)
                companieDataToSave['qtd_notas_entradas_operacao_dori'] = analyzeIfFieldIsValid(amountNotaEntrada, 'qtd_notas_operacao_dori', 0)
                companieDataToSave['qtd_notas_servicos_operacao'] = analyzeIfFieldIsValid(amountNotaServico, 'qtd_notas_operacao', 0)
                companieDataToSave['qtd_notas_servicos_operacao_dori'] = analyzeIfFieldIsValid(amountNotaServico, 'qtd_notas_operacao_dori', 0)               

                companieDataToSave['codi_emp'] = codiEmp
                companieDataToSave['cgce_matriz'] = cgceMatriz
                companieDataToSave['competence'] = f'{year}-{month:0>2}'
                
                self._collection.update_one( 
                    { 
                        "codi_emp": companieDataToSave['codi_emp'],
                        "competence": companieDataToSave['competence']
                    }, 
                    { "$set": companieDataToSave }, 
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

                cgceEmp = str(treatNumberField(companieSettingView['cgce_emp']))
                cgceMatriz = cgceEmp[:8]

                isCompanyBranch = treatTextField(companieSettingView['isCompanyBranch'])

                if isCompanyBranch == 'NAO':
                    companieMonthsAmountNotes = self.getCompaniesMonthsAmountNotes(cgceMatriz)
                else:
                    companieMonthsAmountNotes = self.getCompaniesMonthsAmountNotes(cgceEmp)
                
                self.saveMongo(codiEmp, cgceMatriz, companieMonthsAmountNotes)

        except Exception as e:
            print(f"Erro ao executar a consulta. O erro é: {e}")
        finally:
            self._connectionMongo.closeConnection()
            self._DB.closeConnection()


if __name__ == "__main__":
    instanceClass = CompaniesMonthsIntegrated()
    instanceClass.exportData()

