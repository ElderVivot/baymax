# coding: utf-8

import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))
sys.path.append(os.path.join(fileDir, 'backend/accounting_integration/src'))

import json
from services.rules.ReadExcelToExportDataLivroCaixa import ReadExcelToUpdateOrExportData
from services.rules.GenerateExcelLivroCaixa import GenerateExcel
from services.rules.GenerateExportLivroCaixa import GenerateExportDominio

wayToSaveFiles = open(os.path.join(fileDir, 'backend/accounting_integration/src/WayToSaveFiles.json') )
wayDefault = json.load(wayToSaveFiles)
wayToSaveFiles.close()


class UpdateOrExportData(object):
    def __init__(self):
        # self._codiEmp = input(f'\n - Digite o código da empresa dentro da Domínio: ')
        self._codiEmp = 1593
        self._wayFilesToRead = os.path.join(wayDefault['WayToSaveFilesOriginals'], f'{self._codiEmp}/arquivos_processados')

    def process(self):
        for root, dirs, files in os.walk(self._wayFilesToRead):
            if root == self._wayFilesToRead:
                for file in files:
                    print(f'\n - Atualizando o arquivo "{file}"')
                    wayFile = os.path.join(root, file)

                    print(f'\t - Etapa 1: Lendo o arquivo original')
                    readExcelToUpdateOrExportData = ReadExcelToUpdateOrExportData(wayFile)
                    livroCaixa = readExcelToUpdateOrExportData.getLivroCaixa()
                    accountPlan = readExcelToUpdateOrExportData.getAccountPlan()

                    print(f'\t - Etapa 2: Exportando informações')
                    generateExportDominio = GenerateExportDominio(self._codiEmp, file, livroCaixa, accountPlan)
                    generateExportDominio.exportLivroCaixa()
                    generateExportDominio.closeFile()

        print('\n - Processo Finalizado.')
        os.system('pause > nul')


if __name__ == "__main__":
    updateOrExportData = UpdateOrExportData()
    updateOrExportData.process()
