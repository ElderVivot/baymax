# coding: utf-8

import pandas as pd
import pyodbc
import os
import json
from db.ConexaoBanco import DB
# from functions.usefulFunctions import parseTypeFiedValueCorrect

fileDir = os.path.dirname(os.path.realpath('__file__'))

class extractEfentradas():
    def __init__(self):
        self._DB = DB()
        self._connection = self._DB.getConnection()
        self._cursor = None
        self._wayCompanies = os.path.join(fileDir, 'extract/data/empresas.json')

    def exportaDados(self, filterCompanie=1, filterMonthStart=1, filterYearStart=2018):
        with open(self._wayCompanies) as companies:
            data = json.load(companies)
            for companie in data:
                self._wayToSave = os.path.join(fileDir, f"extract/data/{companie['codi_emp']}-efentradas.json")
                
                # only companies actives
                if companie['stat_emp'] not in ('I') and companie['dina_emp'] is None:
                    if companie['codi_emp'] == filterCompanie or filterCompanie == 0:
                        try:
                            self._cursor = self._connection.cursor()
                            sql = ( f"SELECT codi_emp, codi_ent, nume_ent, codi_for, codi_esp, codi_acu, codi_nat, segi_ent, seri_ent, dent_ent, ddoc_ent, vcon_ent "
                                    f"  FROM bethadba.efentradas "
                                    f" WHERE codi_emp = {companie['codi_emp']}"
                                    f"   AND year(dent_ent) >= {filterYearStart}"
                                    f"   AND month(dent_ent) >= {filterMonthStart}"
                                    f"ORDER BY codi_emp, codi_ent")
                            self._cursor.execute(sql)

                            df = pd.read_sql_query(sql, self._connection)

                            df.to_json(self._wayToSave, orient='records', date_format='iso' ) 
                        except Exception as e:
                            print(f"Erro ao executar a consulta. O erro é: {e}")
                        finally:
                            if self._cursor is not None:
                                self._cursor.close()
                            self._DB.closeConnection()