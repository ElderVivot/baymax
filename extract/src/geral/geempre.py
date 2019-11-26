# coding: utf-8

import pandas as pd
import pyodbc
import os
from db.ConexaoBanco import DB
# from functions.usefulFunctions import parseTypeFiedValueCorrect

fileDir = os.path.dirname(os.path.realpath('__file__'))

class extractGeempre():
    def __init__(self):
        self._DB = DB()
        self._connection = self._DB.getConnection()
        self._cursor = None
        self._wayToSave = os.path.join(fileDir, 'extract/data/empresas.json') 
        self._columns = []

    def exportaDados(self):
        try:
            self._cursor = self._connection.cursor()
            sql = ("SELECT * FROM bethadba.geempre WHERE stat_emp NOT IN ('I') AND dina_emp IS NOT NULL ORDER BY codi_emp")
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


