import os
import sys

absPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(absPath[:absPath.find('extract')])

import json
import pandas as pd
from extract.src.db.ConexaoBanco import DB
from tools.leArquivos import readSql

class GetNaturezaConta():
    def __init__(self, codi_emp):
        self._DB = DB()
        self._connection = self._DB.getConnection()
        self._codi_emp = codi_emp

    def get(self):
        try:
            sql = readSql(os.path.dirname(os.path.abspath(__file__)), 'get_natureza_conta.sql', self._codi_emp)
            df = pd.read_sql_query(sql, self._connection)
            data = json.loads(df.to_json(orient='records', date_format='iso'))

            return data
        except Exception as e:
            print(e)
        finally:
            self._DB.closeConnection()