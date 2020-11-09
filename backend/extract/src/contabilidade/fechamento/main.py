import os
import sys

absPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(absPath[:absPath.find('extract')])

from datetime import datetime
from tools.funcoesUteis import retornaCampoComoData
from process_competences import ProcessCompetences

class MainFechamento():
    def __init__(self):
        self._startDate = retornaCampoComoData(input('Informe o data inicial (dd/mm/aaaa): '))#retornaCampoComoData('01/01/2019')
        self._endDate = retornaCampoComoData(input('Informe o data final (dd/mm/aaaa): '))

        processCompetences = ProcessCompetences(self._startDate, self._endDate)
        processCompetences.process()


if __name__ == "__main__":
    mainFechamento = MainFechamento()
    