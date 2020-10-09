import os
import sys

absPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(absPath[:absPath.find('extract')])

from datetime import datetime
from extract.src.functions.extractFunctions import returnMonthsOfYear
from get_companies import GetCompanies
from process_natureza_conta import ProcessNaturezaConta

class ProcessCompetences():
    def __init__(self, startDate: datetime, endDate: datetime):
        self._startDate = startDate
        self._endDate = endDate

    def process(self):
        year = self._startDate.year
        startYear = self._startDate.year
        startMonth = self._startDate.month
        endYear = self._endDate.year
        endMonth = self._endDate.month

        while year <= endYear:
            months = returnMonthsOfYear(year, startMonth, startYear, endMonth, endYear)
            
            for month in months:

                if month in (3,6,9,12):
                    getCompanies = GetCompanies(f'{year}-{month:0>2}-01')
                    companies = getCompanies.get()
                else:
                    continue

                process_natureza_conta = ProcessNaturezaConta(year, month, companies)
                process_natureza_conta.process()

            print('')
            year += 1
