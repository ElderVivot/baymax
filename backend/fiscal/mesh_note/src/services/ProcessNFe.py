import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
# absPath = "C:/Programming/baymax"
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import datetime
# from model.Issuer import Emitente
# from model.Destinatario import Destinatario
# from model.NotaFiscal import NotaFiscal
from tools.leArquivos import readXml, readJson
import tools.funcoesUteis as funcoesUteis
from zipfile import ZipFile
from rarfile import RarFile
from py7zr import SevenZipFile

class ProcessNFe(object):
    def __init__(self, wayToRead):
        self._wayToRead = wayToRead
        self._companies = readJson(os.path.join(fileDir, 'backend/extract/data/empresas.json'))

    def returnDataEmp(self, cgce):
        for companie in self._companies:
            if companie["cgce_emp"] == cgce and companie["stat_emp"] == "A" and companie["dina_emp"] is None:
                return companie["codi_emp"]

    def process(self, xml):
        dataXml = readXml(xml)

        keyNF = funcoesUteis.returnDataFieldInDict(dataXml, ['nfeProc', 'NFe', 'infNFe', '@Id'])
        keyNF = keyNF[3:]
        
        numberNF = funcoesUteis.returnDataFieldInDict(dataXml, ['nfeProc', 'NFe', 'infNFe', 'ide', 'nNF'])
        issueDateNF = funcoesUteis.returnDataFieldInDict(dataXml, ['nfeProc', 'NFe', 'infNFe', 'ide', 'dhEmi'])
        issueDateNF = funcoesUteis.retornaCampoComoData(issueDateNF, 2)

        modelNF = funcoesUteis.returnDataFieldInDict(dataXml, ['nfeProc', 'NFe', 'infNFe', 'ide', 'mod'])
        serieNF = funcoesUteis.returnDataFieldInDict(dataXml, ['nfeProc', 'NFe', 'infNFe', 'ide', 'serie'])
        valueNF = funcoesUteis.returnDataFieldInDict(dataXml, ['nfeProc', 'NFe', 'infNFe', 'total', 'ICMSTot', 'vNF'])
        valueICMS = funcoesUteis.returnDataFieldInDict(dataXml, ['nfeProc', 'NFe', 'infNFe', 'total', 'ICMSTot', 'vICMS'])
        cnpjIssuer = funcoesUteis.returnDataFieldInDict(dataXml, ['nfeProc', 'NFe', 'infNFe', 'emit', 'CNPJ'])
        nameIssuer = funcoesUteis.returnDataFieldInDict(dataXml, ['nfeProc', 'NFe', 'infNFe', 'emit', 'xNome'])
        cnpjReceiver = funcoesUteis.returnDataFieldInDict(dataXml, ['nfeProc', 'NFe', 'infNFe', 'dest', 'CNPJ'])
        cpfReceiver = funcoesUteis.returnDataFieldInDict(dataXml, ['nfeProc', 'NFe', 'infNFe', 'dest', 'CPF'])
        nameReceiver = funcoesUteis.returnDataFieldInDict(dataXml, ['nfeProc', 'NFe', 'infNFe', 'dest', 'xNome'])

    def rearrangeWayToSaveXML(self, xml):
        dataXml = readXml(xml)
        
        keyNF = funcoesUteis.returnDataFieldInDict(dataXml, ['nfeProc', 'NFe', 'infNFe', '@Id'])
        keyNF = keyNF[3:]
        
        issueDateNF = funcoesUteis.returnDataFieldInDict(dataXml, ['nfeProc', 'NFe', 'infNFe', 'ide', 'dhEmi'])
        issueDateNF = funcoesUteis.retornaCampoComoData(issueDateNF, 2)

        typeNF = funcoesUteis.returnDataFieldInDict(dataXml, ['nfeProc', 'NFe', 'infNFe', 'ide', 'tpNF'])
        
        cnpjIssuer = funcoesUteis.returnDataFieldInDict(dataXml, ['nfeProc', 'NFe', 'infNFe', 'emit', 'CNPJ'])
        cpfIssuer = funcoesUteis.returnDataFieldInDict(dataXml, ['nfeProc', 'NFe', 'infNFe', 'emit', 'CPF'])
        cnpjIssuer = cpfIssuer if cnpjIssuer == "" else cnpjIssuer
        
        cnpjReceiver = funcoesUteis.returnDataFieldInDict(dataXml, ['nfeProc', 'NFe', 'infNFe', 'dest', 'CNPJ'])
        cpfReceiver = funcoesUteis.returnDataFieldInDict(dataXml, ['nfeProc', 'NFe', 'infNFe', 'dest', 'CPF'])
        cnpjReceiver = cpfReceiver if cnpjReceiver == "" else cnpjReceiver

        if typeNF == "0": # quem emitiu foi quem comprou a nota, então o dest vira o emit
            cnpjIssuerCorrect = cnpjReceiver
            cnpjReceiverCorrect = cnpjIssuer
        else:
            cnpjIssuerCorrect = cnpjIssuer
            cnpjReceiverCorrect = cnpjReceiver

        codiEmpIssuer = self.returnDataEmp(cnpjIssuerCorrect)
        codiEmpReceiver = self.returnDataEmp(cnpjReceiverCorrect)

        funcoesUteis.copyXmlToFolderCompanieAndCompetence('X:/', codiEmpIssuer, issueDateNF, xml, 'Saidas', keyNF)
        funcoesUteis.copyXmlToFolderCompanieAndCompetence('X:/', codiEmpReceiver, issueDateNF, xml, 'Entradas', keyNF)

    def processAll(self, processingType):
        # processingType = 1 lê as notas pra comparar com o sistema; quando igual a 2 reestrutura o caminho dos xmls
        for root, dirs, files in os.walk(self._wayToRead):
            countFiles = len(files)
            for key, file in enumerate(files):
                wayFile = os.path.join(root, file)
                if file.lower().endswith(('.xml')):
                    print(f'- Processando XML {file} / {key+1} de {countFiles}')
                    if processingType == 2:
                        self.rearrangeWayToSaveXML(wayFile)
                # if file.lower().endswith(('.zip')):
                #     with ZipFile(wayFile, 'r') as compressed:
                #         for fileCompressed in compressed.namelist():
                #             if fileCompressed.lower().endswith(('.xml')):
                #                 print(fileCompressed)

if __name__ == "__main__":
    processNFe = ProcessNFe("Y:/6-PASTA PUBLICA/XMLs")
    # processNFe.rearrangeWayToSaveXML("C:/_temp/notas-fiscais/52191206217735000158550010000822341551822348.xml")
    processNFe.processAll(2)