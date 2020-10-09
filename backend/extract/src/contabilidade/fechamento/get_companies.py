import os
import sys

absPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(absPath[:absPath.find('extract')])

import json
import pandas as pd
from extract.src.db.ConexaoBanco import DB
from tools.leArquivos import readSql

class GetCompanies():
    def __init__(self, competence):
        self._DB = DB()
        self._connection = self._DB.getConnection()
        self._competence = competence

    def get(self):
        try:
            sql = readSql(os.path.dirname(os.path.abspath(__file__)), 'get_companies.sql', self._competence)
            df = pd.read_sql_query(sql, self._connection)
            data = json.loads(df.to_json(orient='records', date_format='iso'))

            return data
        except Exception as e:
            print(e)
        finally:
            self._DB.closeConnection()