import sys
import os
import csv

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import json
from tools.leArquivos import readCsv, leXls_Xlsx, ImageToText
import tools.funcoesUteis as funcoesUteis


class Temp(object):
    def __init__(self, wayFile):
        self._wayFile = wayFile

    def process(self):
        
        for root, dirs, files in os.walk(self._wayFile):
            for file in files:
                wayFile = os.path.join(root, file)
                print(wayFile)
                ImageToText(wayFile, 'C:/_temp/robson_imgs/teste')

if __name__ == "__main__":

    temp = Temp('C:/_temp/robson_imgs/teste')
    temp.process()