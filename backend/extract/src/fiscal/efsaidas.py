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
import datetime
from db.ConexaoBanco import DB
from tools.leArquivos import readJson
import tools.funcoesUteis as funcoesUteis
import functions.extractFunctions as extractFunctions

wayToSaveFiles = open(os.path.join(fileDir, 'backend/extract/src/WayToSaveFiles.json') )
wayDefault = json.load(wayToSaveFiles)
wayToSaveFiles.close()

class extractEfsaidas():
    def __init__(self):
        self._DB = DB()
        self._connection = self._DB.getConnection()
        self._cursor = None
        self._wayCompanies = os.path.join(wayDefault['wayDefaultToSaveFiles'], 'empresas.json')
        self._dataCompanies = readJson(self._wayCompanies)
        self._baseWayToSave = os.path.join(wayDefault['wayDefaultToSaveFiles'], 'saidas')
        if os.path.exists(self._baseWayToSave) is False:
            os.makedirs(self._baseWayToSave)
        self._today = datetime.date.today()
        self._currentMonth = self._today.month
        self._currentYear = self._today.year

    def exportData(self, filterCompanie=0, filterMonthStart=1, filterYearStart=2013, filterMonthEnd=0, filterYearEnd=0):
        filterMonthEnd = self._currentMonth if filterMonthEnd == 0 else filterMonthEnd
        filterYearEnd = self._currentYear if filterYearEnd == 0 else filterYearEnd
        
        try:
            for companie in self._dataCompanies:
                codi_emp = companie['codi_emp']

                if filterCompanie != 0 and filterCompanie != codi_emp:
                    continue # ignora as empresas que não estão no filtro

                print(f"- Exportando NF de saídas da empresa {codi_emp} - {companie['nome_emp']}")
                
                wayToSaveCompanie = os.path.join(self._baseWayToSave, str(codi_emp))
                if os.path.exists(wayToSaveCompanie) is False:
                    os.makedirs(wayToSaveCompanie)
                        
                competenceStartEnd = extractFunctions.returnCompetenceStartEnd(companie, filterMonthStart, filterYearStart, filterMonthEnd, filterYearEnd)
                startMonth = competenceStartEnd['filterMonthStart']
                startYear = competenceStartEnd['filterYearStart']
                endMonth = competenceStartEnd['filterMonthEnd']
                endYear = competenceStartEnd['filterYearEnd']

                year = startYear

                while year <= endYear:

                    months = extractFunctions.returnMonthsOfYear(year, startMonth, startYear, endMonth, endYear)

                    print('\t - Competências: ', end='')
                    for month in months:
                        print(f'{month:0>2}/{year}, ', end='')

                        self._wayToSave = os.path.join(wayToSaveCompanie, f'{str(year)}{month:0>2}.json')

                        self._cursor = self._connection.cursor()
                        sql = ( f"SELECT nf.codi_emp, nf.codi_sai, nf.nume_sai, nf.codi_cli, nf.codi_esp, nf.codi_acu, nf.codi_nat, nf.segi_sai, "
                                f"       nf.seri_sai, nf.dsai_sai, nf.ddoc_sai, nf.vcon_sai, nf.situacao_sai "
                                f"  FROM bethadba.efsaidas AS nf "
                                f" WHERE nf.codi_emp = {codi_emp}"
                                f"   AND year(nf.ddoc_sai) = {year}"
                                f"   AND month(nf.ddoc_sai) = {month}"
                                f"ORDER BY nf.codi_emp, nf.codi_sai")
                        self._cursor.execute(sql)

                        df = pd.read_sql_query(sql, self._connection)

                        df.to_json(self._wayToSave, orient='records', date_format='iso' ) 

                    print('')
                    year += 1
                        
        except Exception as e:
            print(f"Erro ao executar a consulta. O erro é: {e}")
        finally:
            if self._cursor is not None:
                self._cursor.close()
            self._DB.closeConnection()


if __name__ == "__main__":
    efsaidas = extractEfsaidas()
    efsaidas.exportData()