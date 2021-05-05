# coding: utf-8

import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))
sys.path.append(os.path.join(fileDir, 'backend/accounting_integration/src'))

import shutil
import json
import tools.leArquivos as leArquivos
import tools.funcoesUteis as funcoesUteis
from services.read_files.Folha.ReadResumoGeralAlterdata import ReadResumoGeralAlterdata
from services.rules.GenerateExcelFolhaPagto import GenerateExcel

wayToSaveFiles = open(os.path.join(fileDir, 'backend/accounting_integration/src/WayToSaveFiles.json') )
wayDefault = json.load(wayToSaveFiles)
wayToSaveFiles.close()


class ProcessIntegration(object):
    def __init__(self):
        # self._codiEmp = int(input(f'\n - Digite o código da empresa dentro da Domínio que será realizada a integração: '))
        self._codiEmp = 1646
        
        self._wayFilesToRead = os.path.join(wayDefault['WayToSaveFilesOriginals'], f'{self._codiEmp}/arquivos_originais')
        

    def process(self):
            
        print('\n - Etapa 1: Lendo as planilhas de resumo')
        readResumoGeral = ReadResumoGeralAlterdata(self._codiEmp, self._wayFilesToRead, [])
        dataResumoGeral = readResumoGeral.processAll()

        print(f' - Etapa 2: Exportando informações')
        generateExcel = GenerateExcel(self._codiEmp, dataResumoGeral)
        generateExcel.sheetFolhaPagto()
        generateExcel.closeFile()
        
        print(' - Processo Finalizado.')
        os.system('pause > nul')


if __name__ == "__main__":
    processIntegration = ProcessIntegration()
    processIntegration.process()