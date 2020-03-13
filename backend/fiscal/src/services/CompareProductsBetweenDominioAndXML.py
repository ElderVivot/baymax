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
    def __init__(self, wayToReadXMLs, filterDate="01/01/2019"):
        self._wayToReadXMLs = wayToReadXMLs
        self._wayToRead = os.path.join(wayToSaveFile, 'entradas_produtos')
        self._filterDate = funcoesUteis.retornaCampoComoData(filterDate)
        self._companies = readJson(os.path.join(wayToSaveFile, 'empresas.json'))

        self._hourProcessing = datetime.datetime.now()
        self._client = MongoClient() # conecta num cliente do MongoDB rodando na sua máquina
        self._db = self._client.baymax
        self._collection = self._db[f'MeshNote']        

    def returnDataEmp(self, codi_emp):
        for companie in self._companies:
            if companie["codi_emp"] == codi_emp and companie["stat_emp"] == "A" and companie["dina_emp"] is None:
                return companie["cgce_emp"]

    def returnDataEntryNoteXML(self, codi_emp, month, year, keyNF):
        try:
            wayXml = os.path.join(self._wayToReadXMLs, f'{codi_emp} -', f'{str(year)}-{month:0>2}', 'Entradas', f'{keyNF}.xml')
            callReadXmls = CallReadXmls(wayXml)
            nf = callReadXmls.process()
            
            produtos = funcoesUteis.analyzeIfFieldIsValid(nf, 'produtos')
            print(produtos)
        except Exception:
            pass

    def returnDataOutputNoteXML(self, codi_emp, month, year, keyNF):
        try:
            nf = CallReadXmls(os.path.join(wayToSaveFile, f'{codi_emp} -', f'{str(year)}-{month:0>2}', 'Entradas', f'{keyNF}.xml'))
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
        nfs = readJson(jsonNF)

        if len(nfs) == 0:
            return ""

        for nf in nfs:
            codi_emp = nf['codi_emp']
            cgce_emp = self.returnDataEmp(codi_emp)
            
            chave_nfe = nf['chave_nfe']

            emissao = nf['emissao']
            emissao = funcoesUteis.retornaCampoComoData(emissao, 2)

            month = emissao.month
            year = emissao.year
            
            # busca os dados das notas de entradas
            if jsonNF.find('entradas_produtos') >= 0:
                self.returnDataEntryNoteXML(codi_emp, month, year, chave_nfe)

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
                    print(f'- Processando JSON {wayFile} / {key+1} de {countFiles}')
                    self.process(wayFile)

if __name__ == "__main__":
    meshNote = MeshNote("C:/_temp/notas-fiscais-2/")
    meshNote.processAll()
