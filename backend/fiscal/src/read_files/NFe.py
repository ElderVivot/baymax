import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import datetime
from tools.leArquivos import readXml, readJson
import tools.funcoesUteis as funcoesUteis


class NFe(object):
    def __init__(self, dataXml):
        self._dataXml = dataXml

    def readNFe(self):
        keyNF = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', '@Id'])
        keyNF = keyNF[3:]
        
        numberNF = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'ide', 'nNF'])
        
        issueDateNF = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'ide', 'dhEmi'])
        issueDateNF2 = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'ide', 'dEmi'])
        issueDateNF = issueDateNF2 if ( issueDateNF == "" or issueDateNF is None ) else issueDateNF
        issueDateNF = funcoesUteis.transformDateFieldToString(funcoesUteis.retornaCampoComoData(issueDateNF, 2))

        modelNF = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'ide', 'mod'])
        serieNF = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'ide', 'serie'])
        valueNF = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'total', 'ICMSTot', 'vNF'])
        valueICMS = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'total', 'ICMSTot', 'vICMS'])
        nameIssuer = funcoesUteis.justLettersNumbersDots(funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'emit', 'xNome']))
        nameReceiver = funcoesUteis.justLettersNumbersDots(funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'dest', 'xNome']))

        typeNF = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'ide', 'tpNF'])
        
        cnpjIssuer = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'emit', 'CNPJ'])
        cpfIssuer = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'emit', 'CPF'])
        cnpjIssuer = cpfIssuer if cnpjIssuer == "" else cnpjIssuer
        
        cnpjReceiver = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'dest', 'CNPJ'])
        cpfReceiver = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'dest', 'CPF'])
        cnpjReceiver = cpfReceiver if cnpjReceiver == "" else cnpjReceiver

        if typeNF == "0": # quem emitiu foi quem comprou a nota, então o dest vira o emit (nota própria)
            cnpjIssuerCorrect = cnpjReceiver
            nameIssuerCorrect = nameReceiver
            cnpjReceiverCorrect = cnpjIssuer
            nameReceiverCorrect = nameIssuer
        else:
            cnpjIssuerCorrect = cnpjIssuer
            nameIssuerCorrect = nameIssuer
            cnpjReceiverCorrect = cnpjReceiver
            nameReceiverCorrect = nameReceiver

        produtos = funcoesUteis.returnDataFieldInDict(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'det'])

        return {
            "numberNF": numberNF,
            "serieNF": serieNF,
            "modelNF": modelNF,
            "typeNF": typeNF,
            "issueDateNF": issueDateNF,
            "valueNF": valueNF,
            "valueICMS": valueICMS,
            "nameIssuer": nameIssuerCorrect,
            "cnpjIssuer": cnpjIssuerCorrect,
            "nameReceiver": nameReceiverCorrect,
            "cnpjReceiver": cnpjReceiverCorrect,
            "keyNF": keyNF,
            "statusNF": 0, # ativa
            "produtos": produtos
        }