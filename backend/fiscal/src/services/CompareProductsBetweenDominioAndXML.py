import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import datetime
import json
import codecs
from pymongo import MongoClient
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
        self._wayToRead = os.path.join(wayToSaveFile, 'saidas_produtos')
        self._filterDate = funcoesUteis.retornaCampoComoData(filterDate)
        self._companies = readJson(os.path.join(wayToSaveFile, 'empresas.json'))

        self._hourProcessing = datetime.datetime.now()
        self._client = MongoClient() # conecta num cliente do MongoDB rodando na sua máquina
        self._db = self._client.baymax
        self._collection = self._db[f'MeshNote']        

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

    def saveResultProcessEntryNote(self, dataProcess):
        codi_emp = dataProcess['codiEmpReceiver']
        if codi_emp is None:
            return None

        existsProcessNF = self._collection.find_one( { "$and": [ {"codiEmp": codi_emp}, {"hourProcessing": self._hourProcessing }, {"typeNF": "ENT" }, {"keyNF": dataProcess['keyNF'] } ] } )
        if existsProcessNF is None:
            self._collection.insert_one(
                {
                    "codiEmp": codi_emp,
                    "keyNF": dataProcess['keyNF'],
                    "hourProcessing": self._hourProcessing,
                    "typeNF": "ENT",
                    "nfXml": dataProcess['nfXml'],
                    "nfDominio": dataProcess['nfEntryNoteDominio'],
                    "wayXml": dataProcess['wayXml']
                }
            )

    def saveResultProcessOutputNote(self, dataProcess):
        codi_emp = dataProcess['codiEmpIssuer']
        if codi_emp is None:
            return None

        existsProcessNF = self._collection.find_one( { "$and": [ {"codiEmp": codi_emp}, {"hourProcessing": self._hourProcessing }, {"typeNF": "SAI" }, {"keyNF": dataProcess['keyNF'] } ] } )
        if existsProcessNF is None:
            self._collection.insert_one(
                {
                    "codiEmp": codi_emp,
                    "keyNF": dataProcess['keyNF'],
                    "hourProcessing": self._hourProcessing,
                    "typeNF": "SAI",
                    "nfXml": dataProcess['nfXml'],
                    "nfDominio": dataProcess['nfOutputNoteDominio'],
                    "wayXml": dataProcess['wayXml']
                }
            )

    def process(self, jsonNF):
        nf = readJson(jsonNF)

        if len(nf) == 0:
            return ""

        # cnpjIssuer = funcoesUteis.analyzeIfFieldIsValid(nf, 'cnpjIssuer')
        # cnpjReceiver = funcoesUteis.analyzeIfFieldIsValid(nf, 'cnpjReceiver')
        # issueDate = funcoesUteis.retornaCampoComoData(funcoesUteis.analyzeIfFieldIsValid(nf, 'issueDateNF'), 2)
        # keyNF = funcoesUteis.analyzeIfFieldIsValid(nf, 'keyNF')

        # monthIssueDateNF = issueDate.month
        # yearIssueDateNF = issueDate.year

        # codiEmpIssuer = self.returnDataEmp(cnpjIssuer)
        # codiEmpReceiver = self.returnDataEmp(cnpjReceiver)
        
        # outputNoteDominio = None
        # entryNoteDominio = None

        # if codiEmpIssuer is not None:
        #     outputNoteDominio = self.returnDataOutputNoteDominio(codiEmpIssuer, monthIssueDateNF, yearIssueDateNF, keyNF)

        # if codiEmpReceiver is not None:
        #     entryNoteDominio = self.returnDataEntryNoteDominio(codiEmpReceiver, monthIssueDateNF, yearIssueDateNF, keyNF)

        # dataProcessNF = {
        #     "codiEmpIssuer": codiEmpIssuer,
        #     "codiEmpReceiver": codiEmpReceiver,
        #     "keyNF": keyNF,
        #     "nfXml": nf,
        #     "nfEntryNoteDominio": entryNoteDominio,
        #     "nfOutputNoteDominio": outputNoteDominio,
        #     "wayXml": xml.replace('\\', '/')
        # }

        # self.saveResultProcessEntryNote(dataProcessNF)
        # self.saveResultProcessOutputNote(dataProcessNF)
    
    def processAll(self):
        for root, dirs, files in os.walk(self._wayToRead):
            countFiles = len(files)
            for key, file in enumerate(files):
                wayFile = os.path.join(root, file)
                if file.lower().endswith(('.json')):
                    print(f'- Processando XML {wayFile} / {key+1} de {countFiles}')
                    self.process(wayFile)
                # if file.lower().endswith(('.zip')):
                #     with ZipFile(wayFile, 'r') as compressed:
                #         for fileCompressed in compressed.namelist():
                #             if fileCompressed.lower().endswith(('.xml')):
                #                 print(fileCompressed)

if __name__ == "__main__":
    meshNote = MeshNote("C:/_temp/notas-fiscais-2/413 -/2019-07/Saidas")
    meshNote.processAll()
