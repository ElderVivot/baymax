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
from difflib import SequenceMatcher
from operator import itemgetter
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

    def foundProductInNote(self, productsXML, nameProductAccountSystem, qtdAccountSystem, vunitAccountSystem, vtotAccountSystem):
        productsEquals = []

        for productXML in productsXML:
            nameProductXML = funcoesUteis.treatTextField(productXML['prod']['xProd'])
            qtdProductXML = funcoesUteis.treatDecimalField(productXML['prod']['qCom'])
            vunitProductXML = funcoesUteis.treatDecimalField(productXML['prod']['vUnCom'])
            vtotProductXML = funcoesUteis.treatDecimalField(productXML['prod']['vProd'])

            if qtdProductXML == qtdAccountSystem and vunitProductXML == vunitAccountSystem and vtotProductXML == vtotAccountSystem:
                productXML['valueComparationBetweenAccountSystemAndXML'] = SequenceMatcher(None, nameProductAccountSystem, nameProductXML).ratio()
                if productXML['valueComparationBetweenAccountSystemAndXML'] > 0.75:
                    return productXML
                else:
                    productsEquals.append(productXML)
                print(productXML)

        # print(productsEquals)
        # print( sorted(productsEquals, key=itemgetter('valueComparationBetweenAccountSystemAndXML')) )

    def returnProductComparation(self, productAccountSystem, productsXML):
        if len(productsXML) == 0:
            return None

        nameProductAccountSystem = funcoesUteis.treatTextField(productAccountSystem['desc_pdi'])
        qtdAccountSystem = funcoesUteis.treatDecimalField(productAccountSystem['qtd'])
        vunitAccountSystem = funcoesUteis.treatDecimalField(productAccountSystem['vunit'])
        vtotAccountSystem = funcoesUteis.treatDecimalField(productAccountSystem['vtot'])

        productXML = None
        
        if len(productsXML) == 1:
            productXML = productsXML[0]
            nameProductXML = funcoesUteis.treatTextField(productXML['prod']['xProd'])
            productXML['valueComparationBetweenAccountSystemAndXML'] = SequenceMatcher(None, nameProductAccountSystem, nameProductXML).ratio()
        else:
            productXML = self.foundProductInNote(productsXML, nameProductAccountSystem, qtdAccountSystem, vunitAccountSystem, vtotAccountSystem)

        return productXML

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
        nf = ''
        productsXML = []
        typeNF = ''

        products = readJson(jsonNF)

        if len(products) == 0:
            return ""

        for key, product in enumerate(products):
            codi_emp = product['codi_emp']

            cgce_emp = self.returnDataEmp(codi_emp)
            
            keyNF = product['chave_nfe']

            emissao = product['emissao']
            emissao = funcoesUteis.retornaCampoComoData(emissao, 2)

            month = emissao.month
            year = emissao.year

            previousProduct = funcoesUteis.analyzeIfFieldIsValidMatrix(products, key-1)
            previousKeyNF = previousProduct['chave_nfe']
            
            # busca os dados das notas de entradas
            if jsonNF.find('entradas_produtos') >= 0:
                typeNF = 'Entradas'
            if jsonNF.find('saidas_produtos') >= 0:
                typeNF = 'Saidas'

            if keyNF != previousKeyNF or len(products) == 1:
                wayXml = os.path.join(self._wayToReadXMLs, f'{codi_emp} -', f'{str(year)}-{month:0>2}', f'{typeNF}', f'{keyNF}.xml')
                callReadXmls = CallReadXmls(wayXml)
                nf = callReadXmls.process()
                
                productsXML = funcoesUteis.analyzeIfFieldIsValid(nf, 'produtos')
                
                # quando existe apenas um produto no XML ele não cria um array de produtos, e sim apenas um objeto. Todavia, pra função de
                # comparação funcionar preciso que seja um array. As linhas abaixo fazem esta análise e cria o array quando necessário
                productsWhenExistOneProductXML = []
                onlyProductInXML = funcoesUteis.analyzeIfFieldIsValid(productsXML, 'prod', False)
                if onlyProductInXML is not False:
                    productsWhenExistOneProductXML.append(productsXML)
                    productsXML = productsWhenExistOneProductXML

            productXML = self.returnProductComparation(product, productsXML)

            nameProductAccountSystem = funcoesUteis.treatTextField(product['desc_pdi'])
            # nameProductXML = funcoesUteis.treatTextField(productXML['prod']['xProd'])
            # valueComparation = productXML['valueComparationBetweenAccountSystemAndXML']

            print(keyNF, '---', nameProductAccountSystem, '---', )

            nameProductXML = funcoesUteis.treatTextField(productXML['prod']['xProd'])                

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
