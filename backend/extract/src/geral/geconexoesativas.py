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
from apscheduler.schedulers.blocking import BlockingScheduler
# from functions.usefulFunctions import parseTypeFiedValueCorrect

class extractGeConexoesAtivas():
    def __init__(self):
        self._DB = DB()
        self._connection = self._DB.getConnection()
        self._cursor = None
        self._columns = []

        self._hourProcessing = datetime.now()
        self._connectionMongo = ConnectMongo()
        self._dbMongo = self._connectionMongo.getConnetion()
        self._collection = self._dbMongo['ExtractConnectionsDominioActive']

    def exportData(self):
        try:
            self._cursor = self._connection.cursor()
            sql = ("SELECT * FROM bethadba.geconexoesativas ORDER BY usuario")
            self._cursor.execute(sql)

            df = pd.read_sql_query(sql, self._connection)

            data = json.loads(df.to_json(orient='records', date_format='iso'))
            for connectionActive in data:
                connectionActive['hourProcess'] = self._hourProcessing
                self._collection.insert_one(connectionActive)

        except Exception as e:
            print(f"Erro ao executar a consulta. O erro é: {e}")
        finally:
            if self._cursor is not None:
                self._cursor.close()
            self._DB.closeConnection()
            self._connectionMongo.closeConnection()


if __name__ == "__main__":

    def instantiateObject():
        geconexoesativas = extractGeConexoesAtivas()
        geconexoesativas.exportData()
        print('Dados exportados')

    scheduler = BlockingScheduler()
    scheduler.add_job(instantiateObject, 'interval', seconds=30)
    scheduler.start()

