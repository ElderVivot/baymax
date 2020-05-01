# coding: utf-8

import os
import sys

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend/extract/src'))
sys.path.append(os.path.join(fileDir, 'backend'))

import pandas as pd
import pyodbc
import json
from datetime import datetime
from db.ConexaoBanco import DB
from dao.src.ConnectMongo import ConnectMongo
# from functions.usefulFunctions import parseTypeFiedValueCorrect

wayToSaveFiles = open(os.path.join(fileDir, 'backend/extract/src/WayToSaveFiles.json') )
wayDefault = json.load(wayToSaveFiles)
wayDefaultToSave = wayDefault['wayDefaultToSaveFiles']
wayToSaveFiles.close()
if os.path.exists(wayDefaultToSave) is False:
    os.makedirs(wayDefaultToSave)

class extractGeempre():
    def __init__(self):
        self._DB = DB()
        self._connection = self._DB.getConnection()
        self._cursor = None
        self._wayToSave = os.path.join(wayDefaultToSave, 'empresas.json') 
        self._columns = []

        self._connectionMongo = ConnectMongo()
        self._dbMongo = self._connectionMongo.getConnetion()
        self._collection = self._dbMongo['ExtractCompanies']

    def exportData(self):
        try:
            self._cursor = self._connection.cursor()
            sql = ("  SELECT emp.codi_emp, emp.apel_emp, emp.nome_emp, emp.razao_emp, emp.cgce_emp, emp.tins_emp, emp.stat_emp, emp.dcad_emp, emp.dina_emp,"
                   "         emp.dtinicio_emp, emp.dddf_emp, emp.fone_emp, emp.email_emp, emp.i_cnae20, emp.ramo_emp, emp.rleg_emp, emp.esta_emp,"
                   "         COALESCE( mun.nome_municipio, '' ) AS nome_municipio_emp,"
                   "         COALESCE( vig.rfed_par, 0 ) AS regime_emp,"
                   "         COALESCE( CASE WHEN regime_emp IS NULL THEN ''"
                   "                        WHEN regime_emp IN (2,4) THEN vig.simplesn_regime_par"
                   "                        ELSE federais_regime_par"
                   "                   END, 'C' ) AS regime_caixa_emp"
                   "    FROM bethadba.geempre AS emp"
                   "         LEFT OUTER JOIN bethadba.gemunicipio AS mun"
                   "                   ON    mun.codigo_municipio = emp.codigo_municipio"
                   "         LEFT OUTER JOIN bethadba.efparametro_vigencia AS vig"
                   "                   ON    vig.codi_emp = emp.codi_emp"
                   "   WHERE vig.vigencia_par = ( SELECT MAX(vig2.vigencia_par)"
                   "                                FROM bethadba.efparametro_vigencia AS vig2"
                   "                               WHERE vig2.codi_emp = vig.codi_emp"
                   "                                 AND vig2.vigencia_par <= today() )"
                   "ORDER BY emp.codi_emp")
            self._cursor.execute(sql)

            df = pd.read_sql_query(sql, self._connection)

            data = json.loads(df.to_json(orient='records', date_format='iso'))
            print('- Exportando empresas:')
            for companie in data:
                self._collection.update_one( { "codi_emp": companie['codi_emp'] }, { "$set": companie}, upsert=True )
                print(f"\t-{companie['codi_emp']} - {companie['razao_emp']}")

            df.to_json(self._wayToSave, orient='records', date_format='iso' )
        except Exception as e:
            print(f"Erro ao executar a consulta. O erro é: {e}")
        finally:
            if self._cursor is not None:
                self._cursor.close()
            self._DB.closeConnection()
            # self._connectionMongo.closeConnection()


if __name__ == "__main__":
    geempre = extractGeempre()
    geempre.exportData()

