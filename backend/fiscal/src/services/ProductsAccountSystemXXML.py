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

class ProductsAccountSystemXXML(object):
    def __init__(self, filterDate="01/01/2019"):
        self._wayToReadXMLs = input('- Informe a pasta onde estão os XMLs que servirão como base na comparação: ')
        self._wayToRead = [os.path.join(wayToSaveFile, 'entradas_produtos'), os.path.join(wayToSaveFile, 'saidas_produtos')]
        self._filterDate = funcoesUteis.retornaCampoComoData(filterDate)
        self._companies = readJson(os.path.join(wayToSaveFile, 'empresas.json'))

        self._hourProcessing = datetime.datetime.now()
        self._client = MongoClient() # conecta num cliente do MongoDB rodando na sua máquina
        self._db = self._client.baymax
        self._collection = self._db[f'ProductComparationBetweenAccountSystemAndXML']        

    def returnDataEmp(self, codi_emp):
        for companie in self._companies:
            if companie["codi_emp"] == codi_emp and companie["stat_emp"] == "A" and companie["dina_emp"] is None:
                return companie["cgce_emp"]

    def foundProductInNote(self, productsXML, nameProductAccountSystem, qtdAccountSystem, vunitAccountSystem):
        productsEquals = []

        for productXML in productsXML:
            nameProductXML = funcoesUteis.treatTextField(productXML['prod']['xProd'])
            qtdProductXML = round(funcoesUteis.treatDecimalField(productXML['prod']['qCom']),2)
            vunitProductXML = round(funcoesUteis.treatDecimalField(productXML['prod']['vUnCom']),2)
            # vtotProductXML = round(funcoesUteis.treatDecimalField(productXML['prod']['vProd']),2)

            if qtdProductXML == qtdAccountSystem and vunitProductXML == vunitAccountSystem:
                productXML['valueComparationBetweenAccountSystemAndXML'] = SequenceMatcher(None, nameProductAccountSystem, nameProductXML).ratio()
                if productXML['valueComparationBetweenAccountSystemAndXML'] > 0.85:
                    return productXML
                else:
                    productsEquals.append(productXML)

        if len(productsEquals) > 0:
            return sorted(productsEquals, key=itemgetter('valueComparationBetweenAccountSystemAndXML'))[0]

    def returnProductComparation(self, productAccountSystem, productsXML):
        if len(productsXML) == 0:
            return None

        nameProductAccountSystem = funcoesUteis.treatTextField(productAccountSystem['desc_pdi'])
        qtdAccountSystem = round(funcoesUteis.treatDecimalField(productAccountSystem['qtd']),2)
        vunitAccountSystem = round(funcoesUteis.treatDecimalField(productAccountSystem['vunit']),2)
        vtotAccountSystem = round(funcoesUteis.treatDecimalField(productAccountSystem['vtot']),2)

        productXML = None
        
        if len(productsXML) == 1:
            productXML = productsXML[0]
            nameProductXML = funcoesUteis.treatTextField(productXML['prod']['xProd'])
            productXML['valueComparationBetweenAccountSystemAndXML'] = SequenceMatcher(None, nameProductAccountSystem, nameProductXML).ratio()
        else:
            productXML = self.foundProductInNote(productsXML, nameProductAccountSystem, qtdAccountSystem, vunitAccountSystem)

        return productXML

    def saveResultProcess(self, dataProcess):
        filterProcess = { "$and": [ {"codiEmp": dataProcess['codiEmp']}, {"typeNF": dataProcess['typeNF'] }, {"keyNF": dataProcess['keyNF'] } ] }
        self._collection.replace_one(filterProcess, dataProcess, upsert=True)

    def process(self, jsonNF):
        nf = ''
        productsXML = []
        typeNF = ''
        noteHasProducts = False

        products = readJson(jsonNF)

        if len(products) == 0:
            return ""

        for key, product in enumerate(products):
            codi_emp = product['codi_emp']

            cgce_emp = self.returnDataEmp(codi_emp)
            # ignora empresas inativas
            if cgce_emp is None:
                continue
            
            keyNF = product['chave_nfe']
            # ignora notas que não são NF-e
            if keyNF == "" or keyNF is None:
                continue

            emissao = product['emissao']
            emissao = funcoesUteis.retornaCampoComoData(emissao, 2)

            month = emissao.month
            year = emissao.year

            previousProduct = funcoesUteis.analyzeIfFieldIsValidMatrix(products, key-1)
            previousKeyNF = funcoesUteis.analyzeIfFieldIsValid(previousProduct, 'chave_nfe')
            
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

                noteHasProducts = False if len(productsXML) == 0 else True
                
                # quando existe apenas um produto no XML ele não cria um array de produtos, e sim apenas um objeto. Todavia, pra função de
                # comparação funcionar preciso que seja um array. As linhas abaixo fazem esta análise e cria o array quando necessário
                productsWhenExistOneProductXML = []
                onlyProductInXML = funcoesUteis.analyzeIfFieldIsValid(productsXML, 'prod', False)
                if onlyProductInXML is not False:
                    productsWhenExistOneProductXML.append(productsXML)
                    productsXML = productsWhenExistOneProductXML

            productXML = self.returnProductComparation(product, productsXML)
            if productXML is not None:
                valueComparationBetweenAccountSystemAndXML = productXML['valueComparationBetweenAccountSystemAndXML']
                
                # deleta o campo pois pra remover o productXML do arrays de products as informações tem que ser idênticas
                del productXML['valueComparationBetweenAccountSystemAndXML']
                
                # remove o produto pra ele não processar 2 vezes dizendo como seria de outro produto
                productsXML.remove(productXML)
            else:
                valueComparationBetweenAccountSystemAndXML = 0

            if valueComparationBetweenAccountSystemAndXML <= 0.3 and noteHasProducts is True:
                dataProcess = {
                    "codiEmp": codi_emp,
                    "keyNF": keyNF,
                    "typeNF": typeNF[:3].upper(),
                    "productDominio": product,
                    "productXML": productXML,
                    "valueComparationBetweenAccountSystemAndXML": valueComparationBetweenAccountSystemAndXML
                }

                self.saveResultProcess(dataProcess)
    
    def processAll(self):
        for wayToRead in self._wayToRead:
            for root, dirs, files in os.walk(wayToRead):
                countFiles = len(files)
                for key, file in enumerate(files):
                    wayFile = os.path.join(root, file)
                    if file.lower().endswith(('.json')):
                        print(f'- Processando JSON {wayFile} / {key+1} de {countFiles}')
                        self.process(wayFile)

if __name__ == "__main__":
    productsAccountSystemXXML = ProductsAccountSystemXXML()
    productsAccountSystemXXML.processAll()
