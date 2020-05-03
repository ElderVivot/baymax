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
import datetime
from db.ConexaoBanco import DB
from dao.src.ConnectMongo import ConnectMongo
from tools.leArquivos import readJson, readSql
import tools.funcoesUteis as funcoesUteis
import functions.extractFunctions as extractFunctions

# wayToSaveFiles = open(os.path.join(fileDir, 'backend/extract/src/WayToSaveFiles.json') )
# wayDefault = json.load(wayToSaveFiles)
# wayToSaveFiles.close()

class extractEfmvepro():
    def __init__(self):
        self._DB = DB()
        self._connection = self._DB.getConnection()
        self._cursor = None
        # self._baseWayToSave = os.path.join(wayDefault['wayDefaultToSaveFiles'], 'entradas_produtos')
        # if os.path.exists(self._baseWayToSave) is False:
        #     os.makedirs(self._baseWayToSave)
        self._today = datetime.date.today()
        self._currentMonth = self._today.month
        self._currentYear = self._today.year

        self._connectionMongo = ConnectMongo()
        self._dbMongo = self._connectionMongo.getConnetion()
        self._collection = self._dbMongo['ExtractEntryNoteProducts']

    def getCompanies(self):
        try:
            self._cursor = self._connection.cursor()
            sql = "SELECT codi_emp, nome_emp FROM bethadba.geempre WHERE stat_emp = 'A' ORDER BY codi_emp"
            self._cursor.execute(sql)

            df = pd.read_sql_query(sql, self._connection)

            data = json.loads(df.to_json(orient='records', date_format='iso'))

            return data

        except Exception as e:
            print(f"Erro ao executar a consulta. O erro é: {e}")
        finally:
            if self._cursor is not None:
                self._cursor.close()

    def exportData(self, filterCompanie=0, filterMonthStart=5, filterYearStart=2015, filterMonthEnd=0, filterYearEnd=0):
        filterMonthEnd = self._currentMonth if filterMonthEnd == 0 else filterMonthEnd
        filterYearEnd = self._currentYear if filterYearEnd == 0 else filterYearEnd

        try:
            companies = self.getCompanies()

            for companie in companies:
                codi_emp = companie['codi_emp']

                if filterCompanie != 0 and filterCompanie != codi_emp:
                    continue # ignora as empresas que não estão no filtro

                print(f"- Exportando produtos das NF de entradas da empresa {codi_emp} - {companie['nome_emp']}")
                
                # wayToSaveCompanie = os.path.join(self._baseWayToSave, str(codi_emp))
                # if os.path.exists(wayToSaveCompanie) is False:
                #     os.makedirs(wayToSaveCompanie)
                        
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

                        # self._wayToSave = os.path.join(wayToSaveCompanie, f'{str(year)}{month:0>2}.json')

                        # tem que deletar os dados mensais, pois não dá pra atualizar as informações, visto que o codi_ent que seria
                        # o item a ser atualizado pode mudar na domínio. Antes uma nota que era 100 pode ser excluída, e a 100 ser 
                        # outra nota totalmente diferente
                        self._collection.delete_many( {"$and": [{'codi_emp': companie['codi_emp']}, {'monthFilter': month}, {'yearFilter': year}] } )

                        self._cursor = self._connection.cursor()
                        sql = readSql(os.path.dirname(os.path.abspath(__file__)), 'efmvepro.sql', year, month, companie['codi_emp'], year, month)
                        self._cursor.execute(sql)

                        df = pd.read_sql_query(sql, self._connection)
                        
                        data = json.loads(df.to_json(orient='records', date_format='iso'))
                        if len(data) > 0:
                            self._collection.insert_many( data )

                    print('')
                    year += 1
                        
        except Exception as e:
            print(f"Erro ao executar a consulta. O erro é: {e}")
        finally:
            if self._cursor is not None:
                self._cursor.close()
            self._DB.closeConnection()
            self._connectionMongo.closeConnection()


if __name__ == "__main__":
    extract = extractEfmvepro()
    extract.exportData()