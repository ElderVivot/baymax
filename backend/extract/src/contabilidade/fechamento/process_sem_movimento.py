import os
import sys

absPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(absPath[:absPath.find('extract')])

from calendar import monthrange
from get_sem_movimento import GetSemMovimento
from save_process_db import SaveProcessDb

class ProcessSemMovimento():
    def __init__(self, year, month, companies):
        self._year = year
        self._month = month
        self._companies = companies

    def startAndDate(self, companie):
        last_day_end_date = monthrange(self._year, self._month)[1]  
        end_date = f"{self._year}-{self._month:0>2}-{last_day_end_date:0>2}"
        competence = end_date[:7]

        if companie['regime_emp'] in (2, 4):
            start_date = f"{self._year}-01-01"
        else:
            start_date = f"{self._year}-{(self._month-2):0>2}-01"

        if companie['dina_emp'] is not None:            
            dina_emp = companie['dina_emp'][:10]
            dina_emp_int = dina_emp.replace('-', '')

            start_date_int = start_date.replace('-', '')
            end_date_int = end_date.replace('-', '')
            if start_date_int <= dina_emp_int and dina_emp_int <= end_date_int:
                end_date = dina_emp

        return [start_date, end_date, competence]

    def sendToSave(self, dataSemMovimento):
        saveProcessDb = SaveProcessDb(dataSemMovimento, 'AccountMovimentoProFechamento')
        saveProcessDb.save()

    def process(self):
        for companie in self._companies:
            if self._year <= 2021 and companie['regime_emp'] in (2, 4) and self._month in (3, 6, 9):
                continue
            
            hasMovimento = True
            startAndDate = self.startAndDate(companie)
            startDate = startAndDate[0]
            endDate = startAndDate[1]
            competence = startAndDate[2]
            
            getSemMovimento = GetSemMovimento()
            dataSemMovimento = getSemMovimento.get(companie['codi_emp'], startDate, endDate)[0]
            if dataSemMovimento['total_notas'] == 0 and dataSemMovimento['lan_contabil'] == 0 and dataSemMovimento['calc_folha'] == 0:
                hasMovimento = False

            dataSemMovimento['competence'] = competence
            dataSemMovimento['has_movimento'] = hasMovimento

            self.sendToSave(dataSemMovimento)

            print(f"- Exportado empresa {companie['codi_emp']} - {companie['nome_emp']} | período {startDate} à {endDate}")
