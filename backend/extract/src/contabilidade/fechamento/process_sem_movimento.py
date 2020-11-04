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
        if companie['regime_emp'] in (2, 4):
            start_date = f"{self._year}-01-01"
        else:
            start_date = f"{self._year}-{(self._month-2):0>2}-01"
        return [start_date, end_date]

    def sendToSave(self, dataSemMovimento):
        saveProcessDb = SaveProcessDb(dataSemMovimento, 'AccountFechamento')
        saveProcessDb.save()

    def process(self):
        for companie in self._companies:
            if self._year == 2019 and companie['regime_emp'] in (2, 4) and self._month in (3, 6, 9):
                continue
            
            hasMovimento = True
            startAndDate = self.startAndDate(companie)
            startDate = startAndDate[0]
            endDate = startAndDate[1]
            
            getSemMovimento = GetSemMovimento()
            dataSemMovimento = getSemMovimento.get(companie['codi_emp'], startDate, endDate)[0]
            if dataSemMovimento['total_notas'] == 0 or dataSemMovimento['lan_contabil'] == 0 or dataSemMovimento['lan_contabil'] == 0:
                hasMovimento = False

            dataSemMovimento['competence'] = endDate[:7]
            dataSemMovimento['has_movimento'] = hasMovimento

            self.sendToSave(dataSemMovimento)

            print(f"- Exportado empresa {companie['codi_emp']} - {companie['nome_emp']} | mês {dataSemMovimento['competence']}")
