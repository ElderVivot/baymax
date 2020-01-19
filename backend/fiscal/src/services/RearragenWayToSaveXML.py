import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import datetime
import json
import shutil
from fiscal.src.read_files.CallReadXmls import CallReadXmls
from tools.leArquivos import readXml, readJson
import tools.funcoesUteis as funcoesUteis

wayDefault = readJson(os.path.join(fileDir, 'backend/extract/src/WayToSaveFiles.json') )
wayToSaveFile = wayDefault['wayDefaultToSaveFiles']

class RearrangeWayToSaveXML(object):
    def __init__(self, wayToRead, filterDate="01/01/2019"):
        self._wayToRead = wayToRead
        self._filterDate = funcoesUteis.retornaCampoComoData(filterDate)
        self._companies = readJson(os.path.join(wayToSaveFile, 'empresas.json'))

    def returnDataEmp(self, cgce):
        for companie in self._companies:
            if companie["cgce_emp"] == cgce and companie["stat_emp"] == "A" and companie["dina_emp"] is None:
                return companie["codi_emp"]

    def copyXmlToFolderCompanieAndCompetence(self, wayBase, codiEmp, issueDate, wayXml, typeNF, keyNF):
        if codiEmp is None:
            return None

        wayToSaveXml = os.path.join(wayBase, f'{str(codiEmp)} -', f'{issueDate.year}-{issueDate.month:0>2}', typeNF)
        if os.path.exists(wayToSaveXml) is False:
            os.makedirs(wayToSaveXml)

        shutil.copy(wayXml, os.path.join(wayToSaveXml, f'{keyNF}.xml'))
        print(f'\t- É uma nota de {typeNF[:len(typeNF)]} da empresa {codiEmp}.')
    
    def process(self, xml):
        callReadXmls = CallReadXmls(xml)
        nf = callReadXmls.process()

        cnpjIssuer = funcoesUteis.analyzeIfFieldIsValid(nf, 'cnpjIssuer')
        cnpjReceiver = funcoesUteis.analyzeIfFieldIsValid(nf, 'cnpjReceiver')
        issueDate = funcoesUteis.retornaCampoComoData(funcoesUteis.analyzeIfFieldIsValid(nf, 'issueDateNF'), 2)
        keyNF = funcoesUteis.analyzeIfFieldIsValid(nf, 'keyNF')

        if issueDate < self._filterDate:
            return ""

        codiEmpIssuer = self.returnDataEmp(cnpjIssuer)
        codiEmpReceiver = self.returnDataEmp(cnpjReceiver)
        
        self.copyXmlToFolderCompanieAndCompetence('X:/', codiEmpIssuer, issueDate, xml, 'Saidas', keyNF)
        self.copyXmlToFolderCompanieAndCompetence('X:/', codiEmpReceiver, issueDate, xml, 'Entradas', keyNF)

    def processAll(self):
        for root, dirs, files in os.walk(self._wayToRead):
            countFiles = len(files)
            for key, file in enumerate(files):
                wayFile = os.path.join(root, file)
                if file.lower().endswith(('.xml')):
                    print(f'- Processando XML {wayFile} / {key+1} de {countFiles}')
                    self.process(wayFile)

if __name__ == "__main__":
    rearrangeWayToSaveXML = RearrangeWayToSaveXML("C:/_temp/notas-fiscais")
    rearrangeWayToSaveXML.processAll()
