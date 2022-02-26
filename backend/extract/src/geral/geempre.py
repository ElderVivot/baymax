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
from tools.leArquivos import readSql, readJson
# from functions.usefulFunctions import parseTypeFiedValueCorrect

envData = readJson(os.path.join(fileDir, 'backend/env.json'))
wayDefaultToSave = envData['folderToSaveFilesData']
if os.path.exists(wayDefaultToSave) is False:
    os.makedirs(wayDefaultToSave)

class ExtractGeempre():
    def __init__(self):
        self._DB = DB()
        self._connection = self._DB.getConnection()
        self._wayToSave = os.path.join(wayDefaultToSave, 'empresas.json') 
        self._columns = []

        self._connectionMongo = ConnectMongo()
        self._dbMongo = self._connectionMongo.getConnetion()
        self._collection = self._dbMongo['ExtractCompanies']

    def getCompanies(self):
        try:
            sql = "SELECT codi_emp, nome_emp FROM bethadba.geempre ORDER BY codi_emp"
            df = pd.read_sql_query(sql, self._connection)
            data = json.loads(df.to_json(orient='records', date_format='iso'))

            return data

        except Exception as e:
            print(f"Erro ao executar a consulta. O erro é: {e}")
        finally:
            self._DB.closeConnection()

    def exportData(self):
        try:
            sql = readSql(os.path.dirname(os.path.abspath(__file__)), 'geempre.sql')
            df = pd.read_sql_query(sql, self._connection)
            data = json.loads(df.to_json(orient='records', date_format='iso'))

            print('- Exportando empresas:')
            for companie in data:
                self._collection.update_one( { "codi_emp": companie['codi_emp'] }, { "$set": companie}, upsert=True )
                print(f"\t-{companie['codi_emp']} - {companie['razao_emp']}")

            df.to_json(self._wayToSave, orient='records', date_format='iso' )
        except Exception as e:
            print(f"Erro ao executar a consulta. O erro é: {e}")
        finally:
            self._DB.closeConnection()
            self._connectionMongo.closeConnection()


if __name__ == "__main__":
    geempre = ExtractGeempre()
    geempre.exportData()

