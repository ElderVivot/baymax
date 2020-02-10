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
from services.read_files.LivroCaixaRural import LivroCaixaRural
from services.rules.GenerateExcelLivroCaixa import GenerateExcel

wayToSaveFiles = open(os.path.join(fileDir, 'backend/accounting_integration/src/WayToSaveFiles.json') )
wayDefault = json.load(wayToSaveFiles)
wayToSaveFiles.close()


class ProcessIntegration(object):
    def __init__(self):
        self._codiEmp = int(input(f'\n - Digite o código da empresa dentro da Domínio que será realizada a integração: '))
        # self._codiEmp = 1342
        
        self._wayFilesToRead = os.path.join(wayDefault['WayToSaveFilesOriginals'], f'{self._codiEmp}/arquivos_originais')
        

    def process(self):
            
        print('\n - Etapa 1: Lendo os backups do Livro Caixa Rural')
        livroCaixaRural = LivroCaixaRural(self._codiEmp, self._wayFilesToRead)
        livrosCaixas = livroCaixaRural.processAll()

        print(f' - Etapa 2: Exportando informações')
        generateExcel = GenerateExcel(self._codiEmp)
        generateExcel.sheetLivroCaixa(livrosCaixas[0])
        generateExcel.sheetAccountPlan(livrosCaixas[1])
        generateExcel.closeFile()
        
        print(' - Processo Finalizado.')
        os.system('pause > nul')


if __name__ == "__main__":
    processIntegration = ProcessIntegration()
    processIntegration.process()