# coding: utf-8

import pandas as pd
import pyodbc
import os
import json
from db.ConexaoBanco import DB
# from functions.usefulFunctions import parseTypeFiedValueCorrect

fileDir = os.path.dirname(os.path.realpath('__file__'))

wayToSaveFiles = open(os.path.join(fileDir, 'backend/extract/src/WayToSaveFiles.json') )
wayDefault = json.load(wayToSaveFiles)
wayToSaveFiles.close()

class extractEfentradaspar():
    def __init__(self):
        self._DB = DB()
        self._connection = self._DB.getConnection()
        self._cursor = None
        self._wayCompanies = os.path.join(wayDefault['wayDefaultToSaveFiles'], 'empresas.json') 

    def exportData(self, filterCompanie=0):
        with open(self._wayCompanies) as companies:
            data = json.load(companies)
            try:
                for companie in data:
                    self._wayToSave = os.path.join(wayDefault['wayDefaultToSaveFiles'], f"entradas_parcelas/{companie['codi_emp']}-efentradaspar.json")
                    
                    # only companies actives
                    if companie['stat_emp'] not in ('I') and companie['dina_emp'] is None:
                        if companie['codi_emp'] == filterCompanie or filterCompanie == 0:
                            print(f"- Exportando effornece da empresa {companie['codi_emp']} - {companie['nome_emp']}")
                            self._cursor = self._connection.cursor()
                            sql = ( f"SELECT  "
                                    f"  FROM bethadba.efentradaspar AS par "
                                    f"       INNER JOIN bethadba.efentradas AS ent "
                                    f"            ON    ent.codi_emp = pro.codi_emp "
                                    f"              AND ent.codi_ent = pro.codi_ent "
                                    f" WHERE ent.codi_emp = {companie['codi_emp']}"
                                    f"   AND year(ent.dent_ent) >= {filterYearStart}"
                                    f"   AND month(ent.dent_ent) >= {filterMonthStart}"
                                    f"ORDER BY pro.codi_emp, pro.codi_ent, pro.nume_mep")
                            self._cursor.execute(sql)

                            df = pd.read_sql_query(sql, self._connection)

                            df.to_json(self._wayToSave, orient='records', date_format='iso' ) 
            except Exception as e:
                print(f"Erro ao executar a consulta. O erro é: {e}")
            finally:
                if self._cursor is not None:
                    self._cursor.close()
                self._DB.closeConnection()