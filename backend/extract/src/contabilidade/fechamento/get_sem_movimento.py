import os
import sys

absPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(absPath[:absPath.find('extract')])

import json
import pandas as pd
from extract.src.db.ConexaoBanco import DB
from tools.leArquivos import readSql

class GetSemMovimento():
    def __init__(self):
        self._DB = DB()
        self._connection = self._DB.getConnection()

    def get(self, codi_emp, start_date, end_date):
        try:
            sql = readSql(
                os.path.dirname(os.path.abspath(__file__)), 
                'get_sem_movimento.sql', 
                start_date, end_date, codi_emp
            )
            df = pd.read_sql_query(sql, self._connection)
            data = json.loads(df.to_json(orient='records', date_format='iso'))

            return data
        except Exception as e:
            print(e)

    def closeConnection(self):
        self._DB.closeConnection()