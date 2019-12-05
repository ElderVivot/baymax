import sys
import os

fileDir = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(os.path.join(fileDir, 'backend'))
sys.path.append(os.path.join(fileDir, 'backend/accounting_integration/src/services'))

import json
from datetime import datetime, timedelta
from tools.leArquivos import leXls_Xlsx, leTxt, readJson
import tools.funcoesUteis as funcoesUteis
from read_files.PaymentsCDI import PaymentsCDI
from read_files.SispagItau import SispagItau
from read_files.ExtractsOFX import ExtractsOFX


class ComparePaymentsFinalWithDataBase(object):
    
    def __init__(self, providers, entryNotes=[]):
        self._providers = providers
        self._entryNotes = entryNotes
        self._listWordsNotConsiderInTheName = ['LTDA', '-', 'ME', 'EPP', 'EIRELI', 'MEI', 'EI', 'S.A.', 'SA', 'S.A']

    def removeWordsThatAreNotNames(self, name):
        nameChanged = ""
        for wordName in name.split():
            def chechWordIsInTheList():
                for listWordNotConsider in self._listWordsNotConsiderInTheName:
                    if wordName == listWordNotConsider:
                        return True
            
            if chechWordIsInTheList() is None:
                nameChanged = f"{nameChanged} {wordName}"
        nameChanged = funcoesUteis.minimalizeSpaces(nameChanged)

        return nameChanged       

    def returnDataProvider(self, codi_for=0, cgce='', name=''):

        for provider in self._providers:

            if provider['codi_for'] == codi_for:
                return provider

            if provider['cgce_for'] == cgce:
                return provider

            nameProvider = self.removeWordsThatAreNotNames(provider["nome_for"])
            nameArgument = self.removeWordsThatAreNotNames(name)

            countNameProvider = len(nameProvider.split())
     
            def findProviderForName():
                countEqualWords = 0
                nameArgumentSplit = nameArgument.split(' ')
                for wordName in nameArgumentSplit:
                    if nameProvider.count(wordName) > 0:
                        countEqualWords += 1
                
                if countNameProvider == countEqualWords:
                    return provider
                
                if countNameProvider >= 3:
                    if countNameProvider <= float(countEqualWords):
                        return provider
                
                

            if findProviderForName() is not None:
                return provider

    def returnDataEntryNote(self, note=0, nameProvider='', cgceProvider='', ddoc_ent = None, dent_ent = None, amountPayment = 0.0):

        for entryNote in self._entryNotes:
            provider = self.returnDataProvider(entryNote["codi_for"])
            
            if int(entryNote['nume_ent']) == note and provider["cgce_for"] == cgceProvider:
                return entryNote

            if int(entryNote['nume_ent']) == note and entryNote["ddoc_ent"] == ddoc_ent:
                return entryNote

            if int(entryNote['nume_ent']) == note and entryNote["dent_ent"] == dent_ent:
                return entryNote

            if int(entryNote['nume_ent']) == note and float(entryNote["vcon_ent"]) == amountPayment:
                return entryNote

            if entryNote['ddoc_ent'] == ddoc_ent and provider["cgce_for"] == cgceProvider:
                return entryNote

            if entryNote["dent_ent"] == dent_ent and provider["cgce_for"] == cgceProvider:
                return entryNote
            
            if float(entryNote["vcon_ent"]) == amountPayment and provider["cgce_for"] == cgceProvider:
                return entryNote


if __name__ == "__main__":
    providers = readJson(os.path.join(fileDir, 'backend/extract/data/fornecedores/1117-effornece.json'))
    entryNotes = readJson(os.path.join(fileDir, 'backend/extract/data/entradas/1117-efentradas.json'))
    # print(entryNotes)
    comparePaymentsFinalWithDataBase = ComparePaymentsFinalWithDataBase(providers, entryNotes)
    # comparePaymentsFinalWithDataBase.removeWordsThatAreNotNames(name='LEXUS ENGENHARIA LTDA')
    print(comparePaymentsFinalWithDataBase.returnDataProvider(name='LEXUS ENGENHARIA'))
    # print(comparePaymentsFinalWithDataBase.returnDataProvider(5, "07939369000103"))
    # print(comparePaymentsFinalWithDataBase.returnDataEntryNote(164, '', "07939369000103"))