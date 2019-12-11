# coding: utf-8

import os
import sys

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend/extract/src'))

import pandas as pd
import pyodbc
import json
from db.ConexaoBanco import DB
# from functions.usefulFunctions import parseTypeFiedValueCorrect

wayToSaveFiles = open(os.path.join(fileDir, 'backend/extract/src/WayToSaveFiles.json') )
wayDefault = json.load(wayToSaveFiles)
wayToSaveFiles.close()

class extractGeempre():
    def __init__(self):
        self._DB = DB()
        self._connection = self._DB.getConnection()
        self._cursor = None
        self._wayToSave = os.path.join(wayDefault['wayDefaultToSaveFiles'], 'empresas.json') 
        self._columns = []

    def exportData(self):
        try:
            self._cursor = self._connection.cursor()
            sql = ("SELECT * FROM bethadba.geempre WHERE stat_emp NOT IN ('I') AND dina_emp IS NULL ORDER BY codi_emp")
            self._cursor.execute(sql)

            row = self._cursor.fetchone()
            for header in row.cursor_description:
                self._columns.append(header[0])

            df = pd.read_sql_query(sql, self._connection)

            # df = parseTypeFiedValueCorrect(df, self._columns)

            # df.to_csv(self._caminhoSalvarCSV, header=True, sep='|',float_format='%g',decimal='.', encoding='Windows-1252', na_rep='(null)', index=None)
            df.to_json(self._wayToSave, orient='records', date_format='iso' ) 
        except Exception as e:
            print(f"Erro ao executar a consulta. O erro é: {e}")
        finally:
            if self._cursor is not None:
                self._cursor.close()
            self._DB.closeConnection()


if __name__ == "__main__":
    geempre = extractGeempre()
    geempre.exportData()

