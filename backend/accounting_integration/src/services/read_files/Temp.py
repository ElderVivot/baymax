import sys
import os
import csv

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import json
from tools.leArquivos import readCsv, leXls_Xlsx
import tools.funcoesUteis as funcoesUteis


class Temp(object):
    def __init__(self, wayFile):
        self._wayFile = wayFile

    def process(self):
        dataFile = leXls_Xlsx(self._wayFile)

        classificacaoParte1 = ""
        classificacaoParte2 = ""
        nomeConta = ""
        codigoConta = 0
        codigoContaCorreto = ""
        classificacaoCompleta = ""
        tipoConta = ""

        for data in dataFile:
            classificacaoParte1 = funcoesUteis.treatNumberFieldInVector(data, 1)
            classificacaoParte2 = funcoesUteis.treatNumberFieldInVector(data, 3)
            nomeConta = funcoesUteis.treatTextFieldInVector(data, 6).replace(' .', '')
            if nomeConta != "" and int(classificacaoParte1) > 0:
                if nomeConta[0] == ".":
                    nomeConta = nomeConta[1:].strip()

                if int(classificacaoParte2) == 0:
                    codigoConta += 1
                    codigoContaCorreto = codigoConta
                    classificacaoCompleta = classificacaoParte1
                    tipoConta = "S"
                else:
                    codigoContaCorreto = int(classificacaoParte2)
                    classificacaoCompleta = f'{classificacaoParte1}{classificacaoParte2}'
                    tipoConta = "A"
                
                print(f'{codigoContaCorreto};{classificacaoCompleta};{nomeConta};{tipoConta}')

if __name__ == "__main__":

    temp = Temp('C:/_temp/plano_contas_britago/plano_contas.xlsx')
    temp.process()