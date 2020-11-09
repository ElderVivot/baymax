import sys
import os
import csv

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import json
from tools.leArquivos import readCsv, leXls_Xlsx, ImageToText, leTxt
import tools.funcoesUteis as funcoesUteis


class Temp(object):
    def __init__(self, wayFile):
        self._wayFile = wayFile

    def transformTxt(self, wayFile):
        dataTxt = leTxt(wayFile)
        for data in dataTxt:
            data = funcoesUteis.treatTextField(data)
            if data == '':
                continue
            dataSplit = data.split(' ')

            date = funcoesUteis.treatDateFieldInVector(dataSplit, 1)
            numeroDocumento = funcoesUteis.treatTextFieldInVector(dataSplit, 2)
            creditOrDebit = funcoesUteis.treatTextFieldInVector(dataSplit, 0)
            valorMovimento = funcoesUteis.treatDecimalFieldInVector(dataSplit, -1)
            historico = ' '.join(dataSplit[2:len(dataSplit)-2])
            if valorMovimento > 0:
                dateFormated = funcoesUteis.transformaCampoDataParaFormatoBrasileiro(date)
                print(f'{dateFormated};;;{valorMovimento};;{historico};{numeroDocumento};{creditOrDebit}')

    def readTxts(self):
        for root, dirs, files in os.walk(self._wayFile):
            for file in files:
                wayFile = os.path.join(root, file)
                self.transformTxt(wayFile)

    def transformsImgs(self):        
        for root, dirs, files in os.walk(self._wayFile):
            for file in files:
                wayFile = os.path.join(root, file)
                print(wayFile)
                ImageToText(wayFile, 'C:/_temp/robson_imgs/n_e_materias/txts_pendente')

if __name__ == "__main__":

    temp = Temp('C:/_temp/robson_imgs/n_e_materias/txts_pendente')
    temp.readTxts()