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
from dao.src.ConnectMongo import ConnectMongo
from tools.leArquivos import readJson
import functions.extractFunctions as extractFunctions

wayToSaveFiles = open(os.path.join(fileDir, 'backend/extract/src/WayToSaveFiles.json') )
wayDefault = json.load(wayToSaveFiles)
wayToSaveFiles.close()

class extractAccountBalance():
    def __init__(self):
        self._DB = DB()
        self._connection = self._DB.getConnection()
        self._cursor = None
        self._wayCompanies = os.path.join(wayDefault['wayDefaultToSaveFiles'], 'empresas.json') 
        self._dataCompanies = readJson(self._wayCompanies)
        self._baseWayToSave = os.path.join(wayDefault['wayDefaultToSaveFiles'], 'entradas')
        if os.path.exists(self._baseWayToSave) is False:
            os.makedirs(self._baseWayToSave)
        self._today = datetime.date.today()
        self._currentMonth = self._today.month
        self._currentYear = self._today.year

        self._connectionMongo = ConnectMongo()
        self._dbMongo = self._connectionMongo.getConnetion()
        self._collection = self._dbMongo['AccountBalance']

    def exportData(self, filterCompanie=0, filterMonthStart=1, filterYearStart=2015, filterMonthEnd=0, filterYearEnd=0):
        filterMonthEnd = self._currentMonth if filterMonthEnd == 0 else filterMonthEnd
        filterYearEnd = self._currentYear if filterYearEnd == 0 else filterYearEnd
        
        try:
            for companie in self._dataCompanies:
                codi_emp = companie['codi_emp']

                if filterCompanie != 0 and filterCompanie != codi_emp:
                    continue # ignora as empresas que não estão no filtro

                print(f"- Exportando saldos das contas contábeis da empresa {codi_emp} - {companie['nome_emp']}")
                
                wayToSaveCompanie = os.path.join(self._baseWayToSave, str(codi_emp))
                if os.path.exists(wayToSaveCompanie) is False:
                    os.makedirs(wayToSaveCompanie)
                        
                competenceStartEnd = extractFunctions.returnCompetenceStartEnd(companie, filterMonthStart, filterYearStart, filterMonthEnd, filterYearEnd)
                startYear = competenceStartEnd['filterYearStart']
                endYear = competenceStartEnd['filterYearEnd']

                year = startYear

                while year <= endYear:

                    print(f'\t - {year}', end='')
                    
                    self._cursor = self._connection.cursor()
                    sql = ( "SELECT emp.codi_emp,"
                            "   emp.nome_emp,"
                            "   emp.cgce_emp,"
                            "   con.codi_cta,"		 
                            "   con.nome_cta,"
                            "   con.clas_cta,"
                            "   con.tipo_cta,"
                            "   deb = IF con.tipo_cta = 'S' THEN"
                                      "   IsNull((SELECT sum(l.vlor_lan)" 
                                                "   FROM bethadba.ctlancto AS l"
                                                     "   INNER JOIN bethadba.ctcontas AS c"
                                                          "   ON    c.codi_emp = l.codi_emp" 
                                               "   WHERE l.codi_emp = con.codi_emp"
                                                 f"   AND l.data_lan > DATE('1900-01-01') AND YEAR(l.data_lan) <= {year}"
                                                 "   AND Trim(con.clas_cta) = substr(c.clas_cta, 1, length(con.clas_cta))" 
                                                 "   AND c.codi_cta = l.cdeb_lan), 0)"
                                      "   ELSE"
                                       "   IsNull((SELECT sum(l.vlor_lan)"
                                                "   FROM bethadba.ctlancto AS l"
                                                     "   INNER JOIN bethadba.ctcontas AS c"
                                                          "   ON    c.codi_emp = l.codi_emp"
                                               "   WHERE l.codi_emp = con.codi_emp"
                                                 f"   AND l.data_lan > DATE('1900-01-01') AND YEAR(l.data_lan) <= {year}"
                                                 "   AND c.codi_cta = con.codi_cta"
                                                 "   AND c.codi_cta = l.cdeb_lan), 0) ENDIF,"                          
                            "   cred =  IF con.tipo_cta = 'S' THEN "
                                       "   IsNull((SELECT sum(l.vlor_lan) "
                                                 "   FROM bethadba.ctlancto AS l"
                                                     "   INNER JOIN bethadba.ctcontas AS c"
                                                          "   ON    c.codi_emp = l.codi_emp "
                                               "   WHERE l.codi_emp = con.codi_emp"
                                                  f"   AND l.data_lan > DATE('1900-01-01') AND YEAR(l.data_lan) <= {year}"
                                                  "   AND Trim(con.clas_cta) = substr(c.clas_cta, 1, length(con.clas_cta)) "
                                                  "   AND c.codi_cta = l.ccre_lan), 0)"
                                      "   ELSE "
                                      "   IsNull((SELECT sum(l.vlor_lan) "
                                                 "   FROM bethadba.ctlancto AS l"
                                                     "   INNER JOIN bethadba.ctcontas AS c"
                                                          "   ON    c.codi_emp = l.codi_emp "
                                               "   WHERE l.codi_emp = con.codi_emp"
                                                  f"   AND l.data_lan > DATE('1900-01-01') AND YEAR(l.data_lan) <= {year}"
                                                  "   AND c.codi_cta = con.codi_cta"
                                                  "   AND c.codi_cta = l.ccre_lan), 0) ENDIF,"
                            "   saldo = deb - cred"
                       "   FROM bethadba.ctcontas AS con"
                            "   INNER JOIN bethadba.geempre AS emp"
                                 "   ON    emp.codi_emp = con.codi_emp"     
                      f"   WHERE emp.codi_emp = {codi_emp}"
                      "      AND saldo <> 0"
                   "   ORDER BY emp.codi_emp, con.clas_cta, con.nome_cta" )
                    
                    self._cursor.execute(sql)

                    df = pd.read_sql_query(sql, self._connection)

                    data = json.loads(df.to_json(orient='records', date_format='iso'))
                    for accountBalance in data:
                        accountBalance['year'] = year
                        self._collection.update_one( {
                                "codi_emp": accountBalance['codi_emp'],
                                "codi_cta": accountBalance['codi_cta'],
                                "year": accountBalance['year']
                            },
                            { "$set": accountBalance },
                            upsert=True
                        )


                    print('')
                    year += 1
        except Exception as e:
            print(f"Erro ao executar a consulta. O erro é: {e}")
        finally:
            if self._cursor is not None:
                self._cursor.close()
            self._DB.closeConnection()


if __name__ == "__main__":
    accountBalance = extractAccountBalance()
    accountBalance.exportData()