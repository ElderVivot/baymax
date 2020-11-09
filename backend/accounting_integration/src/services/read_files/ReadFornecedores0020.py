import sys
import os
import csv

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import json
from tools.leArquivos import readCsv, leXls_Xlsx, ImageToText, leTxt
import tools.funcoesUteis as funcoesUteis


class ReadFornecedores(object):
    def __init__(self):
        self._fornecedoresExistLanc = []
        self._fornecedores = []

    def readFornWithAccount(self, wayFile):
        dataTxt = leTxt(wayFile)
        for data in dataTxt:
            dataSplit = data.split(';')
            codiFornecedor = funcoesUteis.treatNumberField(dataSplit[1], isInt=True)
            self._fornecedoresExistLanc.append(codiFornecedor)

    def readFornGenerateDominio(self, wayFile):
        dataTxt = leTxt(wayFile)
        for data in dataTxt:
            dataSplit = data.split('|')
            codiFornecedor = funcoesUteis.treatNumberField(dataSplit[-1], isInt=True)

            if self._fornecedoresExistLanc.count(codiFornecedor) == 0:
                dataSplit[19] = ''

            self._fornecedores.append(dataSplit)
        
        self.generateNewFileForn()

    def generateNewFileForn(self):
        with open('C:/_temp/fornecedores_bono/processar/fornecedores_formatado.txt', 'w') as file:
            for fornecedor in self._fornecedores:
                fornecedor.pop()
                line = f"\n{'|'.join(fornecedor)}"
                file.write(line)


if __name__ == "__main__":
    temp = ReadFornecedores()
    temp.readFornWithAccount('C:/_temp/fornecedores_bono/processar/forn_com_lancamentos.txt')
    temp.readFornGenerateDominio('C:/_temp/fornecedores_bono/processar/fornecedores_atuais.txt')