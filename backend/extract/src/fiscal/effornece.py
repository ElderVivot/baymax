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

class extractEffornece():
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
                    self._wayToSave = os.path.join(wayDefault['wayDefaultToSaveFiles'], 'fornecedores')
                    if os.path.exists(self._wayToSave) is False:
                        os.makedirs(self._wayToSave)
                    self._wayToSave = os.path.join(self._wayToSave, f"{companie['codi_emp']}-effornece.json")
                    
                    # only companies actives
                    if companie['stat_emp'] not in ('I') and companie['dina_emp'] is None:
                        if companie['codi_emp'] == filterCompanie or filterCompanie == 0:
                            print(f"- Exportando fornecedores da empresa {companie['codi_emp']} - {companie['nome_emp']}")
                            self._cursor = self._connection.cursor()
                            sql = ( f"SELECT forn.codi_for, forn.nome_for, forn.nomr_for, forn.cgce_for, forn.codi_cta, forn.insc_for, forn.imun_for, "
                                    f"       forn.codigo_municipio, forn.sigl_est, forn.conta_cliente_for, forn.conta_compensacao_for "
                                    f"  FROM bethadba.effornece AS forn "
                                    f" WHERE forn.codi_emp = {companie['codi_emp']}"
                                    f"ORDER BY forn.codi_emp, forn.codi_for")
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
    effornece = extractEffornece()
    effornece.exportData()