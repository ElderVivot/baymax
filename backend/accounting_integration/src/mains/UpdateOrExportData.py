# coding: utf-8

import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))
sys.path.append(os.path.join(fileDir, 'backend/accounting_integration/src'))

import json
from services.rules.ReadExcelToUpdateOrExportData import ReadExcelToUpdateOrExportData
from services.rules.GenerateExcel import GenerateExcel
from services.rules.GenerateExportDominio import GenerateExportDominio
from services.rules.CompareWithSettings import CompareWithSettings

wayToSaveFiles = open(os.path.join(fileDir, 'backend/accounting_integration/src/WayToSaveFiles.json') )
wayDefault = json.load(wayToSaveFiles)
wayToSaveFiles.close()


class UpdateOrExportData(object):
    def __init__(self):
        self._UpdateOrExport = int(input(f'\n - Para exportar os dados no Leiaute Domínio digite 1, já se quiser atualizar a planilha Financeiro e Extratos pra conferência digite 2: '))
        self._codiEmp = input(f'\n - Digite o código da empresa dentro da Domínio: ')
        # self._codiEmp = 1428
        self._wayFilesToRead = os.path.join(wayDefault['WayToSaveFilesOriginals'], f'{self._codiEmp}/arquivos_processados')

    def process(self):
        for root, dirs, files in os.walk(self._wayFilesToRead):
            if root == self._wayFilesToRead:
                for file in files:
                    print(f'\n - Atualizando o arquivo "{file}"')
                    wayFile = os.path.join(root, file)

                    print(f'\t - Etapa 1: Lendo o arquivo original')
                    readExcelToUpdateOrExportData = ReadExcelToUpdateOrExportData(wayFile)
                    payments = readExcelToUpdateOrExportData.getPayments()
                    extracts = readExcelToUpdateOrExportData.getExtracts()

                    print(f'\t - Etapa 2: Comparando com a planilha de configurações')
                    compareWithSettings = CompareWithSettings(self._codiEmp, payments, extracts, updateOrExtract=True)
                    paymentsCompareWithSettings = compareWithSettings.processPayments()
                    extractsCompareWithSettings = compareWithSettings.processExtracts()
                    
                    print(f'\t - Etapa 3: Exportando informações')
                    if self._UpdateOrExport == 2:
                        generateExcel = GenerateExcel(self._codiEmp, update=True, nameFileUpdate=file)
                        generateExcel.sheetPayments(paymentsCompareWithSettings)
                        generateExcel.sheetExtract(extractsCompareWithSettings)
                        generateExcel.closeFile()
                    else:
                        generateExportDominio = GenerateExportDominio(self._codiEmp, file, paymentsCompareWithSettings, extractsCompareWithSettings)
                        generateExportDominio.exportExtracts()
                        generateExportDominio.exportPayments()
                        generateExportDominio.closeFile()

        print('\n - Processo Finalizado.')
        os.system('pause > nul')


if __name__ == "__main__":
    updateOrExportData = UpdateOrExportData()
    updateOrExportData.process()
