import sys
import os
import csv

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import json
from tools.leArquivos import readCsv
import tools.funcoesUteis as funcoesUteis


class TempFilter(object):
    def __init__(self, wayFile):
        self._wayFile = wayFile

    def process(self):
        dataFile = readCsv(self._wayFile)

        for data in dataFile:
            dateLanc = funcoesUteis.retornaCampoComoData(data[0])
            monthDateLanc = dateLanc.month
            
            nameFile = f'C:/Users/ElderVivot/Downloads/lanc_supermedica/lanc{monthDateLanc:0>2}.txt'

            with open(nameFile, 'a', newline='') as csvfile:
                csvwriter= csv.writer(csvfile, delimiter=';')
                csvwriter.writerow(data)


if __name__ == "__main__":

    tempFilter = TempFilter('C:/Users/ElderVivot/Downloads/lanc_supermedica/2019.txt')
    tempFilter.process()