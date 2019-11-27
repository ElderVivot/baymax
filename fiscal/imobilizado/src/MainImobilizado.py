import os
import sys

fileDir = os.path.dirname(__file__)
sys.path.append(fileDir)

from services.AnalisaNotas import AnalisaNotasImobilizado

# fileDir = os.path.dirname(os.path.realpath('__file__'))

class MainImobilizado:

    # folderData = os.path.join(fileDir, 'extract/data/')

    # for raiz, diretorios, arquivos in os.walk(fileDir):
    #     for arquivo in arquivos:
    #         print(arquivo)

    analisaNotasImobilizado = AnalisaNotasImobilizado()
    

if __name__ == '__main__':
    mainFiscal = MainImobilizado() 
