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

class extractEfmvepro():
    def __init__(self):
        self._DB = DB()
        self._connection = self._DB.getConnection()
        self._cursor = None
        self._wayCompanies = os.path.join(wayDefault['wayDefaultToSaveFiles'], 'empresas.json')
        self._dataCompanies = readJson(self._wayCompanies)
        self._baseWayToSave = os.path.join(wayDefault['wayDefaultToSaveFiles'], 'entradas_produtos')
        if os.path.exists(self._baseWayToSave) is False:
            os.makedirs(self._baseWayToSave)
        self._today = datetime.date.today()
        self._currentMonth = self._today.month
        self._currentYear = self._today.year

    def exportData(self, filterCompanie=2, filterMonthStart=1, filterYearStart=2019, filterMonthEnd=0, filterYearEnd=0):
        filterMonthEnd = self._currentMonth if filterMonthEnd == 0 else filterMonthEnd
        filterYearEnd = self._currentYear if filterYearEnd == 0 else filterYearEnd

        try:
            for companie in self._dataCompanies:
                codi_emp = companie['codi_emp']

                if filterCompanie != 0 and filterCompanie != codi_emp:
                    continue # ignora as empresas que não estão no filtro

                print(f"- Exportando produtos das NF de entradas da empresa {codi_emp} - {companie['nome_emp']}")
                
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

                    print('\t - ', end='')
                    for month in months:
                        print(f'{month:0>2}/{year}, ', end='')

                        self._wayToSave = os.path.join(wayToSaveCompanie, f'{str(year)}{month:0>2}.json')

                        self._cursor = self._connection.cursor()
                        sql = ( f"SELECT pro.codi_emp, codigo_nota = pro.codi_ent, numero = ent.nume_ent, cli_for = forn.nome_for, chave_nfe = ent.chave_nfe_ent, "
                                f"       emissao = ent.ddoc_ent, saida_entrada = ent.dent_ent, codi_pdi = pro.codi_pdi, desc_pdi = procad.desc_pdi, cfop = pro.cfop_mep, "
                                f"       qtd = pro.qtde_mep, vunit = pro.valor_unit_mep, vtot = pro.vlor_mep /*, pro.vipi_mep, pro.bcal_mep, pro.cst_mep, pro.vpro_mep, pro.vdes_mep, pro.bicms_mep, pro.bicmsst_mep, pro.aliicms_mep, pro.valor_icms_mep, pro.valor_subtri_mep, "
                                f"       pro.vfre_mep, pro.vseg_mep, pro.vdesace_mep */ "
                                f"  FROM bethadba.efmvepro AS pro "
                                f"       INNER JOIN bethadba.efentradas AS ent "
                                f"            ON    ent.codi_emp = pro.codi_emp "
                                f"              AND ent.codi_ent = pro.codi_ent "
                                f"       INNER JOIN bethadba.effornece AS forn "
                                f"            ON    forn.codi_emp = ent.codi_emp "
                                f"              AND forn.codi_for = ent.codi_for "
                                f"       INNER JOIN bethadba.efprodutos AS procad "
                                f"            ON    procad.codi_emp = pro.codi_emp "
                                f"              AND procad.codi_pdi = pro.codi_pdi "
                                f" WHERE ent.codi_emp = {codi_emp}"
                                f"   AND year(ent.ddoc_ent) = {year}"
                                f"   AND month(ent.ddoc_ent) = {month}"
                                f"ORDER BY pro.codi_emp, pro.codi_ent, pro.nume_mep")
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
    extract = extractEfmvepro()
    extract.exportData()