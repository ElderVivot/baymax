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

class extractEfmvspro():
    def __init__(self):
        self._DB = DB()
        self._connection = self._DB.getConnection()
        self._cursor = None
        self._wayCompanies = os.path.join(wayDefault['wayDefaultToSaveFiles'], 'empresas.json')
        self._dataCompanies = readJson(self._wayCompanies)
        self._baseWayToSave = os.path.join(wayDefault['wayDefaultToSaveFiles'], 'saidas_produtos')
        if os.path.exists(self._baseWayToSave) is False:
            os.makedirs(self._baseWayToSave)
        self._today = datetime.date.today()
        self._currentMonth = self._today.month
        self._currentYear = self._today.year

    def exportData(self, filterCompanie=0, filterMonthStart=1, filterYearStart=2019, filterMonthEnd=0, filterYearEnd=0):
        filterMonthEnd = self._currentMonth if filterMonthEnd == 0 else filterMonthEnd
        filterYearEnd = self._currentYear if filterYearEnd == 0 else filterYearEnd

        try:
            for companie in self._dataCompanies:
                codi_emp = companie['codi_emp']

                if filterCompanie != 0 and filterCompanie != codi_emp:
                    continue # ignora as empresas que não estão no filtro

                print(f"- Exportando produtos das NF de saídas da empresa {codi_emp} - {companie['nome_emp']}")
                
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
                        sql = ( f"SELECT pro.codi_emp, codigo_nota = pro.codi_sai, numero = sai.nume_sai, cli_for = cli.nome_cli, chave_nfe = sai.chave_nfe_sai, "
                                f"       emissao = sai.ddoc_sai, saida_entrada = sai.dsai_sai, codi_pdi = pro.codi_pdi, desc_pdi = procad.desc_pdi, "
                                f"       cfop = pro.cfop_msp, qtd = pro.qtde_msp, vunit = pro.valor_unit_msp, vtot = pro.vpro_msp /*, pro.vipi_msp, pro.bcal_msp, "
                                f"       pro.cst_msp, pro.vdes_msp, pro.bicms_msp, pro.bicmsst_msp, pro.aliicms_msp, pro.valor_icms_msp, pro.valor_subtri_msp, "
                                f"       pro.vfre_msp, pro.vseg_msp, pro.vdesace_msp */ "
                                f"  FROM bethadba.efmvspro AS pro "
                                f"       INNER JOIN bethadba.efsaidas AS sai "
                                f"            ON    sai.codi_emp = pro.codi_emp "
                                f"              AND sai.codi_sai = pro.codi_sai "
                                f"       INNER JOIN bethadba.efclientes AS cli "
                                f"            ON    cli.codi_emp = sai.codi_emp "
                                f"              AND cli.codi_cli = sai.codi_cli "
                                f"       INNER JOIN bethadba.efprodutos AS procad "
                                f"            ON    procad.codi_emp = pro.codi_emp "
                                f"              AND procad.codi_pdi = pro.codi_pdi "
                                f" WHERE sai.codi_emp = {codi_emp}"
                                f"   AND year(sai.ddoc_sai) = {year}"
                                f"   AND month(sai.ddoc_sai) = {month}"
                                f"ORDER BY pro.codi_emp, pro.codi_sai, pro.nume_msp")
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
    extract = extractEfmvspro()
    extract.exportData()