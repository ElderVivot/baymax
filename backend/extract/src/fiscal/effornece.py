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

class extractEffornece():
    def __init__(self):
        self._DB = DB()
        self._connection = self._DB.getConnection()
        self._cursor = None
        self._wayCompanies = os.path.join(wayDefault['wayDefaultToSaveFiles'], 'empresas.json') 

    def exportaDados(self, filterCompanie=0):
        with open(self._wayCompanies) as companies:
            data = json.load(companies)
            try:
                for companie in data:
                    self._wayToSave = os.path.join(wayDefault['wayDefaultToSaveFiles'], f"fornecedores/{companie['codi_emp']}-effornece.json")
                    
                    # only companies actives
                    if companie['stat_emp'] not in ('I') and companie['dina_emp'] is None:
                        if companie['codi_emp'] == filterCompanie or filterCompanie == 0:
                            print(f"- Exportando effornece da empresa {companie['codi_emp']} - {companie['nome_emp']}")
                            self._cursor = self._connection.cursor()
                            sql = ( f"SELECT forn.codi_for, forn.nome_for, forn.nomr_for, forn.cgce_for, forn.insc_for, forn.imun_for, "
                                    f"       forn.codigo_municipio, forn.sigl_est "
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