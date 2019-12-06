import sys
import os

fileDir = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(os.path.join(fileDir, 'backend'))
sys.path.append(os.path.join(fileDir, 'backend/accounting_integration/src/services'))

import json
from math import floor
from datetime import datetime, timedelta
from tools.leArquivos import leXls_Xlsx, leTxt, readJson
import tools.funcoesUteis as funcoesUteis
from read_files.PaymentsCDI import PaymentsCDI
from read_files.SispagItau import SispagItau
from read_files.ExtractsOFX import ExtractsOFX


class ComparePaymentsFinalWithDataBase(object):
    
    def __init__(self, providers=[], entryNotes=[], payments=[]):
        self._providers = providers
        self._entryNotes = entryNotes
        self._payments = payments
        self._listWordsNotConsiderInTheName = ['LTDA', 'LTDA.', '-', 'ME', 'ME.', 'EPP', 'EPP.', 'EIRELI', 'EIRELI.', \
            'MEI', 'MEI.', 'EI', 'EI.', 'S.A.', 'SA', 'S.A', 'S/A']
        self._listWordsAbbreviatedToChange = {
            "COM.": "COMERCIO",
            "PROD.": "PRODUCAO",
            "IND.": "INDUSTRIA",
            "IMP.": "IMPORTACAO",
            "EXP.": "EXPORTACAO",
            "MAT.": "MATERIAIS",
            "LIMP.": "LIMPEZA",
            "SERV.": "SERVICO",
            "EQUIP.": "EQUIPAMENTOS",
            "P/": "PARA",
            "ARTIG.": "ARTIGOS",
            "DIST.": "DISTRIBUIDORA",
            "CONST.": "CONSTRUCAO"
        }

    def changeAbbreviatedWord(self, name):
        nameChanged = ""
        for wordName in name.split():
            def chechWordIsInTheList():
                for abbreviate, wordToChange in self._listWordsAbbreviatedToChange.items():
                    if wordName == abbreviate:
                        return wordToChange
            
            wordNew = chechWordIsInTheList()
            if wordNew is not None:
                nameChanged = f"{nameChanged} {wordNew}"
            else:
                nameChanged = f"{nameChanged} {wordName}"
        nameChanged = funcoesUteis.minimalizeSpaces(nameChanged)

        return nameChanged
    
    def removeWordsThatAreNotNames(self, name):
        nameChanged = ""
        for wordName in name.split():
            def chechWordIsInTheList():
                for listWordNotConsider in self._listWordsNotConsiderInTheName:
                    if wordName == listWordNotConsider:
                        return True
            
            # adiciona apenas as palavras que não estão na lista
            if chechWordIsInTheList() is None:
                nameChanged = f"{nameChanged} {wordName}"
        nameChanged = funcoesUteis.minimalizeSpaces(nameChanged)

        return nameChanged

    def returnDataProvider(self, codi_for=0, cgce=None, name=None, degreeOfReliability=0):

        for provider in self._providers:

            if int(provider['codi_for']) == int(codi_for):
                return provider

            if provider['cgce_for'] == cgce and cgce is not None:
                return provider

            # agora as verificações pelo nome (esta primeira tem grau alto de confiabilidade)
            if name is None:
                continue

            nameProvider = self.changeAbbreviatedWord(self.removeWordsThatAreNotNames(provider["nome_for"]))
            nameArgument = self.changeAbbreviatedWord(self.removeWordsThatAreNotNames(name))

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
                    if floor(countNameProvider * 0.7) <= countEqualWords:
                        return provider
                else:
                    if nameProvider.count(nameArgument[0:floor(len(nameArgument)*0.75)]) > 0:
                        return provider

                # grau de confibilidade mais baixo, só deve ser usado junto com outra confirmação, como número da nota por exemplo
                if degreeOfReliability == 1:
                    if len(nameArgument) >= 10:
                        if nameProvider.count(nameArgument[0:floor(len(nameArgument)*0.30)]) > 0:
                            return provider
                    else:
                        if nameProvider.count(nameArgument[0:floor(len(nameArgument)*0.60)]) > 0:
                            return provider

            if findProviderForName() is not None:
                return provider

    def returnDataEntryNote(self, note=0, cgceProvider=None, ddoc_ent = None, dent_ent = None, amountPayment = 0.0, nameProvider=None):

        for entryNote in self._entryNotes:
            provider = self.returnDataProvider(entryNote["codi_for"])
            # print(provider)
                    
            # utilizo uma função pois foi precisar comparar o cgce duas vezes, então chamo ele nos dois casos diferentes
            def returnNote(cgceProviderSearch):
                if int(entryNote['nume_ent']) == note and cgceProviderSearch == cgceProvider:
                    return entryNote

                if int(entryNote['nume_ent']) == note and entryNote["ddoc_ent"] == ddoc_ent:
                    return entryNote

                if int(entryNote['nume_ent']) == note and entryNote["dent_ent"] == dent_ent:
                    return entryNote

                if int(entryNote['nume_ent']) == note and float(entryNote["vcon_ent"]) == amountPayment:
                    return entryNote

                if entryNote['ddoc_ent'] == ddoc_ent and cgceProviderSearch == cgceProvider:
                    return entryNote

                if entryNote["dent_ent"] == dent_ent and cgceProviderSearch == cgceProvider:
                    return entryNote
                
                if float(entryNote["vcon_ent"]) == amountPayment and cgceProviderSearch == cgceProvider:
                    return entryNote

            cgce_for = funcoesUteis.analyzeIfFieldIsValid(provider, "cgce_for", None)
            if returnNote(cgce_for) is not None:
                return returnNote(cgce_for)

            # busca a nota olhando pelo nome da empresa
            providerByName = self.returnDataProvider(name=nameProvider, degreeOfReliability=1)
            cgce_for = funcoesUteis.analyzeIfFieldIsValid(providerByName, "cgce_for", None)
            # print(cgce_for)
            print(cgce_for, entryNote["nume_ent"])
            if returnNote(cgce_for) is not None:
                return returnNote(cgce_for)

    # def processComparateWithDataBase(self):
    #     for payment in self._payments:
            


if __name__ == "__main__":
    providers = readJson(os.path.join(fileDir, 'backend/extract/data/fornecedores/1117-effornece.json'))
    entryNotes = readJson(os.path.join(fileDir, 'backend/extract/data/entradas/1117-efentradas.json'))
    # print(entryNotes)
    comparePaymentsFinalWithDataBase = ComparePaymentsFinalWithDataBase(providers, entryNotes)
    # comparePaymentsFinalWithDataBase.removeWordsThatAreNotNames(name='LEXUS ENGENHARIA LTDA')
    # print(comparePaymentsFinalWithDataBase.changeAbbreviatedWord('P/ SERVICO'))
    # print(comparePaymentsFinalWithDataBase.returnDataProvider(name='LEXUS ENGENHARIA'))
    # print(comparePaymentsFinalWithDataBase.returnDataProvider(5, "07939369000103"))
    # print(comparePaymentsFinalWithDataBase.returnDataProvider(5))
    print(comparePaymentsFinalWithDataBase.returnDataEntryNote(164, nameProvider='LEXUS ENGENHARIA'))