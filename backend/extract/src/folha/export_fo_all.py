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

wayToSaveFiles = open(os.path.join(fileDir, 'backend/extract/src/WayToSaveFiles.json') )
wayDefault = json.load(wayToSaveFiles)
wayDefaultToSave = wayDefault['wayDefaultToSaveFiles']
wayDefaultToSave = os.path.join(wayDefaultToSave, 'fo_all')
wayToSaveFiles.close()
if os.path.exists(wayDefaultToSave) is False:
    os.makedirs(wayDefaultToSave)

class extractExportFoAll():
    def __init__(self):
        self._DB = DB()
        self._connection = self._DB.getConnection()
        self._cursor = None
        self._columns = []
        
    def getTables(self):
        try:
            self._cursor = self._connection.cursor()
            sql = readSql(os.path.dirname(os.path.abspath(__file__)), 'tables_db.sql')
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
        cursor = None
        try:
            tables = self.getTables()

            print('- Exportando dados das tabelas:')
            for table in tables:
                table_name = table['table_name']
                print(f'\t- Tabela {table_name}')
                if(table['exist_codi_emp'] is not None):
                    sql = f"SELECT * FROM bethadba.{table_name} WHERE codi_emp IN (1693,1695,1696,1848,1849)"
                else:
                    sql = f"SELECT * FROM bethadba.{table_name}"
                
                cursor = self._connection.cursor()                
                cursor.execute(sql)

                df = pd.read_sql_query(sql, self._connection)
                
                df.to_csv(os.path.join(wayDefaultToSave, f"{table_name}.csv"), index=False, date_format='iso', sep=';', decimal='.', escapechar=None, quotechar='"')

        except Exception as e:
            print(f"Erro ao executar a consulta. O erro é: {e}")
        finally:
            if cursor is not None:
                cursor.close()
            self._DB.closeConnection()


if __name__ == "__main__":
    export = extractExportFoAll()
    export.exportData()

