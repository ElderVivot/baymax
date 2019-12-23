import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import json
import shutil
from tools.leArquivos import readJson, splitPdfOnePageEach, PDFToText
import tools.funcoesUteis as funcoesUteis

wayToSaveFiles = open(os.path.join(fileDir, 'backend/accounting_integration/src/WayToSaveFiles.json') )
wayDefault = json.load(wayToSaveFiles)
wayToSaveFiles.close()


class ReadPDFs(object):

    def __init__(self, codiEmp, wayTemp, wayToRead):
        self._codiEmp = codiEmp
        self._wayTemp = wayTemp
        self._wayToRead = wayToRead
        
    def processSplitPdfOnePageEach(self):
        print('\t - 1.1: Dividindo o PDF em uma página cada pra avaliar se é um PDF scaneado (imagens).')

        sequential = 0 # este sequencial serve pra caso tenha 2 pdfs com mesmo nome em pasta diferentes ele não sobrescreva um ao outro, portanto vai salvar com o nome - sequencial
        
        for root, dirs, files in os.walk(self._wayToRead):
            for file in files:
                if file.lower().endswith(('.pdf')):
                    sequential += 1
                    wayFile = os.path.join(root, file)
                    splitPdfOnePageEach(wayFile, self._wayTemp, sequential)

    def transformPDFToText(self):
        # transform pdfs to text
        print('\t - 1.2: Transformando pra TXTs os PDFs encontrados.')
        for root, dirs, files in os.walk(self._wayTemp):
            for dir_ in dirs:
                if dir_ == "pdfs":
                    wayDir = os.path.join(root, dir_)
                    for rootDir, dirsDir, filesDir in os.walk(wayDir):
                        nameFileSplit = rootDir.split('\\')[-1].split('-')
                        nameFile = '.'.join(nameFileSplit[:-1])
                        if nameFile != "":
                            print(f'\t\t - Arquivo "{nameFile}.pdf"')
                        for file in filesDir:
                            if file.lower().endswith(('.pdf')):
                                wayFile = os.path.join(rootDir, file)
                                wayDirFile = os.path.dirname(wayFile)
                                PDFToText(wayFile, wayDirFile)