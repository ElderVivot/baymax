import os
import sys

absPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(absPath[:absPath.find('extract')])

from datetime import datetime
from tools.funcoesUteis import retornaCampoComoData
from process_competences import ProcessCompetences

class MainFechamento():
    def __init__(self):
        self._startDate = retornaCampoComoData('01/01/2020')
        self._endDate = retornaCampoComoData('30/06/2020')

        processCompetences = ProcessCompetences(self._startDate, self._endDate)
        processCompetences.process()


if __name__ == "__main__":
    mainFechamento = MainFechamento()
    