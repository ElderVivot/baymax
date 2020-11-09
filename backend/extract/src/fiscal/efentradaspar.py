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

wayToSaveFiles = open(os.path.join(fileDir, 'backend/extract/src/WayToSaveFiles.json') )
wayDefault = json.load(wayToSaveFiles)
wayToSaveFiles.close()

class extractEfentradaspar():
    def __init__(self):
        self._DB = DB()
        self._connection = self._DB.getConnection()
        self._cursor = None
        self._wayCompanies = os.path.join(wayDefault['wayDefaultToSaveFiles'], 'empresas.json') 

    def exportData(self, filterCompanie=0, filterMonthStart=1, filterYearStart=2013):
        with open(self._wayCompanies) as companies:
            data = json.load(companies)
            try:
                for companie in data:
                    self._wayToSave = os.path.join(wayDefault['wayDefaultToSaveFiles'])
                    if os.path.exists(self._wayToSave) is False:
                        os.makedirs(self._wayToSave)
                    self._wayToSave = os.path.join(self._wayToSave, f"entradas_parcelas/{companie['codi_emp']}-efentradaspar.json")
                    
                    # only companies actives
                    if companie['codi_emp'] == filterCompanie or filterCompanie == 0:
                        print(f"- Exportando parcelas das NFs de entrada da empresa {companie['codi_emp']} - {companie['nome_emp']}")
                        self._cursor = self._connection.cursor()
                        sql = ( f"SELECT par.codi_emp, par.codi_ent, par.parc_entp, ent.nume_ent, forn.codi_for, ent.ddoc_ent, ent.dent_ent, par.vcto_entp, par.vlor_entp "
                                f"  FROM bethadba.efentradaspar AS par "
                                f"       INNER JOIN bethadba.efentradas AS ent "
                                f"            ON    ent.codi_emp = par.codi_emp "
                                f"              AND ent.codi_ent = par.codi_ent "
                                f"       INNER JOIN bethadba.effornece AS forn "
                                f"            ON    forn.codi_emp = ent.codi_emp "
                                f"              AND forn.codi_for = ent.codi_for "
                                f" WHERE ent.codi_emp = {companie['codi_emp']}"
                                f"   AND year(ent.dent_ent) >= {filterYearStart}"
                                f"   AND month(ent.dent_ent) >= {filterMonthStart}"
                                f"ORDER BY par.codi_emp, ent.dent_ent DESC, par.parc_entp")
                        self._cursor.execute(sql)

                        df = pd.read_sql_query(sql, self._connection)

                        df.to_json(self._wayToSave, orient='records', date_format='iso' ) 
            except Exception as e:
                print(f"Erro ao executar a consulta. O erro é: {e}")
            finally:
                if self._cursor is not None:
                    self._cursor.close()
                self._DB.closeConnection()


if __name__ == "__main__":
    efentradaspar = extractEfentradaspar()
    efentradaspar.exportData()