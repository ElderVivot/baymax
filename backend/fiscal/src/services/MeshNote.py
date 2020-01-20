import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import datetime
import json
import codecs
from fiscal.src.read_files.CallReadXmls import CallReadXmls
from tools.leArquivos import readXml, readJson
import tools.funcoesUteis as funcoesUteis
# from zipfile import ZipFile
# from rarfile import RarFile
# from py7zr import SevenZipFile

wayDefault = readJson(os.path.join(fileDir, 'backend/extract/src/WayToSaveFiles.json') )
wayToSaveFile = wayDefault['wayDefaultToSaveFiles']

class MeshNote(object):
    def __init__(self, wayToRead, filterDate="01/01/2019"):
        self._wayToRead = wayToRead
        self._filterDate = funcoesUteis.retornaCampoComoData(filterDate)
        self._companies = readJson(os.path.join(wayToSaveFile, 'empresas.json'))

    def returnDataEmp(self, cgce):
        for companie in self._companies:
            if companie["cgce_emp"] == cgce and companie["stat_emp"] == "A" and companie["dina_emp"] is None:
                return companie["codi_emp"]

    def returnDataEntryNoteDominio(self, codi_emp, month, year, keyNF):
        try:
            dataNfs = readJson(os.path.join(wayToSaveFile, 'entradas', str(codi_emp), f'{str(year)}{month:0>2}.json'))

            for nf in dataNfs:
                if nf['chave_nfe_ent'] == keyNF:
                    return nf
        except Exception:
            pass

    def returnDataOutputNoteDominio(self, codi_emp, month, year, keyNF):
        try:
            dataNfs = readJson(os.path.join(wayToSaveFile, 'saidas', str(codi_emp), f'{str(year)}{month:0>2}.json'))

            for nf in dataNfs:
                if nf['chave_nfe_sai'] == keyNF:
                    return nf
        except Exception:
            pass

    def saveResultProcessEntryNote(self, dataProcess, hourProcessing):
        codi_emp = dataProcess['codiEmpReceiver']
        if codi_emp is None:
            return None

        wayFileProcessing = os.path.join(fileDir, 'backend/fiscal/data', str(codi_emp), 'entradas')
        if os.path.exists(wayFileProcessing) is False:
            os.makedirs(wayFileProcessing)
        wayFileProcessing = os.path.join(wayFileProcessing, f'{hourProcessing}.json')

        dataFileProcessing = readJson(wayFileProcessing)
        if dataFileProcessing == "" or dataFileProcessing is None:
            dataFileProcessing = []
        
        dataFileProcessing.append({
            "codiEmp": codi_emp,
            "nfXml": dataProcess['nfXml'],
            "nfDominio": dataProcess['nfEntryNoteDominio'],
            "wayXml": dataProcess['wayXml']
        })

        with open(wayFileProcessing, 'w') as outfile:
            json.dump( dataFileProcessing, outfile, indent=4 )

    def saveResultProcessOutputNote(self, dataProcess, hourProcessing):
        codi_emp = dataProcess['codiEmpIssuer']
        if codi_emp is None:
            return None

        wayFileProcessing = os.path.join(fileDir, 'backend/fiscal/data', str(codi_emp), 'saidas')
        if os.path.exists(wayFileProcessing) is False:
            os.makedirs(wayFileProcessing)
        wayFileProcessing = os.path.join(wayFileProcessing, f'{hourProcessing}.json')

        dataFileProcessing = readJson(wayFileProcessing)
        if dataFileProcessing == "" or dataFileProcessing is None:
            dataFileProcessing = []
        
        dataFileProcessing.append({
            "codiEmp": codi_emp,
            "nfXml": dataProcess['nfXml'],
            "nfDominio": dataProcess['nfOutputNoteDominio'],
            "wayXml": dataProcess['wayXml']
        })

        with open(wayFileProcessing, 'w') as outfile:
            json.dump( dataFileProcessing, outfile, indent=4 )

    def process(self, xml, hourProcessing):
        callReadXmls = CallReadXmls(xml)
        nf = callReadXmls.process()

        if nf is None:
            return ""

        cnpjIssuer = funcoesUteis.analyzeIfFieldIsValid(nf, 'cnpjIssuer')
        cnpjReceiver = funcoesUteis.analyzeIfFieldIsValid(nf, 'cnpjReceiver')
        issueDate = funcoesUteis.retornaCampoComoData(funcoesUteis.analyzeIfFieldIsValid(nf, 'issueDateNF'), 2)
        keyNF = funcoesUteis.analyzeIfFieldIsValid(nf, 'keyNF')

        monthIssueDateNF = issueDate.month
        yearIssueDateNF = issueDate.year

        codiEmpIssuer = self.returnDataEmp(cnpjIssuer)
        codiEmpReceiver = self.returnDataEmp(cnpjReceiver)
        
        outputNoteDominio = None
        entryNoteDominio = None

        if codiEmpIssuer is not None:
            outputNoteDominio = self.returnDataOutputNoteDominio(codiEmpIssuer, monthIssueDateNF, yearIssueDateNF, keyNF)

        if codiEmpReceiver is not None:
            entryNoteDominio = self.returnDataEntryNoteDominio(codiEmpReceiver, monthIssueDateNF, yearIssueDateNF, keyNF)

        dataProcessNF = {
            "codiEmpIssuer": codiEmpIssuer,
            "codiEmpReceiver": codiEmpReceiver,
            "nfXml": nf,
            "nfEntryNoteDominio": entryNoteDominio,
            "nfOutputNoteDominio": outputNoteDominio,
            "wayXml": xml.replace('\\', '/')
        }

        self.saveResultProcessEntryNote(dataProcessNF, hourProcessing)
        self.saveResultProcessOutputNote(dataProcessNF, hourProcessing)
    
    def processAll(self):
        hourProcessing = funcoesUteis.getDateTimeNowInFormatStr()
        for root, dirs, files in os.walk(self._wayToRead):
            countFiles = len(files)
            for key, file in enumerate(files):
                wayFile = os.path.join(root, file)
                if file.lower().endswith(('.xml')):
                    print(f'- Processando XML {wayFile} / {key+1} de {countFiles}')
                    self.process(wayFile, hourProcessing)
                # if file.lower().endswith(('.zip')):
                #     with ZipFile(wayFile, 'r') as compressed:
                #         for fileCompressed in compressed.namelist():
                #             if fileCompressed.lower().endswith(('.xml')):
                #                 print(fileCompressed)

if __name__ == "__main__":
    meshNote = MeshNote("C:/_temp/notas-fiscais")
    meshNote.processAll()
