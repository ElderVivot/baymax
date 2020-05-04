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
from extract.src.geral.geempre import ExtractGeempre
from tools.leArquivos import readJson, readSql
import tools.funcoesUteis as funcoesUteis
import functions.extractFunctions as extractFunctions

class extractCtlancto():
    def __init__(self):
        self._DB = DB()
        self._connection = self._DB.getConnection()
        self._cursor = None
        self._today = datetime.date.today()
        self._currentMonth = self._today.month
        self._currentYear = self._today.year
        self._geempre = ExtractGeempre()

        self._connectionMongo = ConnectMongo()
        self._dbMongo = self._connectionMongo.getConnetion()
        self._collection = self._dbMongo['ExtractContasContabeis']

    def exportData(self, filterCompanie=0):
        
        try:
            companies = self._geempre.getCompanies()

            for companie in companies:
                codi_emp = companie['codi_emp']

                if filterCompanie != 0 and filterCompanie != codi_emp:
                    continue # ignora as empresas que não estão no filtro

                print(f"- Exportando as contas contábeis da empresa {codi_emp} - {companie['nome_emp']}")
            
                self._collection.delete_many( {'codi_emp': codi_emp} )

                self._cursor = self._connection.cursor()
                sql = readSql(os.path.dirname(os.path.abspath(__file__)), 'ctcontas.sql', codi_emp)
                self._cursor.execute(sql)

                df = pd.read_sql_query(sql, self._connection)
                
                data = json.loads(df.to_json(orient='records', date_format='iso'))
                if len(data) > 0:
                    self._collection.insert_many( data )
                        
        except Exception as e:
            print(f"Erro ao executar a consulta. O erro é: {e}")
        finally:
            if self._cursor is not None:
                self._cursor.close()
            self._DB.closeConnection()
            self._connectionMongo.closeConnection()


if __name__ == "__main__":
    extract = extractCtlancto()
    extract.exportData()