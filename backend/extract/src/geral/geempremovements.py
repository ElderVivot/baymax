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
from db.ConexaoBanco import DB
from dao.src.ConnectMongo import ConnectMongo
from tools.leArquivos import readSql
# from functions.usefulFunctions import parseTypeFiedValueCorrect

class extractGeempre():
    def __init__(self):
        self._DB = DB()
        self._connection = self._DB.getConnection()
        self._cursor = None
        self._columns = []

        self._connectionMongo = ConnectMongo()
        self._dbMongo = self._connectionMongo.getConnetion()
        self._collection = self._dbMongo['ExtractCompanies'] # vai adicionar na tabela de empresas os dados

    def getCompanies(self):
        try:
            self._cursor = self._connection.cursor()
            sql = "SELECT codi_emp, nome_emp FROM bethadba.geempre ORDER BY codi_emp"
            self._cursor.execute(sql)

            df = pd.read_sql_query(sql, self._connection)

            data = json.loads(df.to_json(orient='records', date_format='iso'))

            return data

        except Exception as e:
            print(f"Erro ao executar a consulta. O erro é: {e}")
        finally:
            if self._cursor is not None:
                self._cursor.close()

    def exportData(self):
        try:
            companies = self.getCompanies()

            print('- Exportando dados de movimentação geral empresas:')
            for companie in companies:
                self._cursor = self._connection.cursor()
                sql = readSql(os.path.dirname(os.path.abspath(__file__)), 'geempremovements.sql', companie['codi_emp'])
                self._cursor.execute(sql)

                df = pd.read_sql_query(sql, self._connection)

                data = json.loads(df.to_json(orient='records', date_format='iso'))[0]
                self._collection.update_one( { "codi_emp": data['codi_emp'] }, { "$set": data}, upsert=True )
                print(f"\t -{companie['codi_emp']} - {companie['nome_emp']}")

        except Exception as e:
            print(f"Erro ao executar a consulta. O erro é: {e}")
        finally:
            if self._cursor is not None:
                self._cursor.close()
            self._DB.closeConnection()
            self._connectionMongo.closeConnection()


if __name__ == "__main__":
    geempre = extractGeempre()
    geempre.exportData()

