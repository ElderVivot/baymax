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
# from functions.usefulFunctions import parseTypeFiedValueCorrect

wayToSaveFiles = open(os.path.join(fileDir, 'backend/extract/src/WayToSaveFiles.json') )
wayDefault = json.load(wayToSaveFiles)
wayDefaultToSave = wayDefault['wayDefaultToSaveFiles']
wayToSaveFiles.close()
if os.path.exists(wayDefaultToSave) is False:
    os.makedirs(wayDefaultToSave)

class extractGeempre():
    def __init__(self):
        self._DB = DB()
        self._connection = self._DB.getConnection()
        self._cursor = None
        self._wayToSave = os.path.join(wayDefaultToSave, 'empresas.json') 
        self._columns = []

        self._connectionMongo = ConnectMongo()
        self._dbMongo = self._connectionMongo.getConnetion()
        self._collection = self._dbMongo['ExtractCompanies']

    def exportData(self):
        try:
            self._cursor = self._connection.cursor()
            sql = ("SELECT * FROM bethadba.geempre ORDER BY codi_emp")
            self._cursor.execute(sql)

            df = pd.read_sql_query(sql, self._connection)

            data = json.loads(df.to_json(orient='records', date_format='iso'))
            for companie in data:
                existsCompanie = self._collection.find_one( { "codi_emp": companie['codi_emp'] } )
                if existsCompanie is None:
                    self._collection.insert_one(companie)
                else:
                    self._collection.update_one( { "codi_emp": companie['codi_emp'] }, { "$set": companie} )

            df.to_json(self._wayToSave, orient='records', date_format='iso' )
        except Exception as e:
            print(f"Erro ao executar a consulta. O erro é: {e}")
        finally:
            if self._cursor is not None:
                self._cursor.close()
            self._DB.closeConnection()
            # self._connectionMongo.closeConnection()


if __name__ == "__main__":
    geempre = extractGeempre()
    geempre.exportData()

