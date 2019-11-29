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

    def exportaDados(self, filterCompanie=0, filterMonthStart=1, filterYearStart=2013):
        with open(self._wayCompanies) as companies:
            data = json.load(companies)
            try:
                for companie in data:
                    self._wayToSave = os.path.join(fileDir, f"extract/data/entradas/{companie['codi_emp']}-efentradas.json")
                    
                    # only companies actives
                    if companie['stat_emp'] not in ('I') and companie['dina_emp'] is None:
                        if companie['codi_emp'] == filterCompanie or filterCompanie == 0:
                            print(f"- Exportando efentradas da empresa {companie['codi_emp']} - {companie['nome_emp']}")
                            self._cursor = self._connection.cursor()
                            sql = ( f"SELECT ent.codi_emp, ent.codi_ent, ent.nume_ent, ent.codi_for, forn.nome_for, ent.codi_esp, ent.codi_acu, ent.codi_nat, ent.segi_ent, "
                                    f"       ent.seri_ent, ent.dent_ent, ent.ddoc_ent, ent.vcon_ent "
                                    f"  FROM bethadba.efentradas AS ent "
                                    f"       INNER JOIN bethadba.effornece AS forn "
                                    f"            ON    forn.codi_emp = ent.codi_emp "
                                    f"              AND forn.codi_for = ent.codi_for "
                                    f" WHERE ent.codi_emp = {companie['codi_emp']}"
                                    f"   AND year(ent.dent_ent) >= {filterYearStart}"
                                    f"   AND month(ent.dent_ent) >= {filterMonthStart}"
                                    f"ORDER BY ent.codi_emp, ent.codi_ent")
                            self._cursor.execute(sql)

                            df = pd.read_sql_query(sql, self._connection)

                            df.to_json(self._wayToSave, orient='records', date_format='iso' ) 
            except Exception as e:
                print(f"Erro ao executar a consulta. O erro é: {e}")
            finally:
                if self._cursor is not None:
                    self._cursor.close()
                self._DB.closeConnection()