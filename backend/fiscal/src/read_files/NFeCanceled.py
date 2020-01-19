import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import datetime
from tools.leArquivos import readXml, readJson
import tools.funcoesUteis as funcoesUteis


class NFeCanceled(object):
    def __init__(self, dataXml):
        self._dataXml = dataXml

    def readNFeCanceled(self):
        keyNF = funcoesUteis.returnDataFieldInDict(self._dataXml, ['procEventoNFe', 'evento', 'infEvento', 'chNFe'])
        
        numberNF = int(keyNF[25:33])
        
        issueDateNF = funcoesUteis.transformDateFieldToString(funcoesUteis.retornaCampoComoData(f'01/{keyNF[4:6]}/20{keyNF[2:4]}'))
        
        modelNF = keyNF[20:22]
        serieNF = keyNF[22:25]
        cnpjIssuer = keyNF[6:20]
        typeNF = keyNF[34]
        
        return {
            "numberNF": numberNF,
            "serieNF": serieNF,
            "modelNF": modelNF,
            "typeNF": typeNF,
            "issueDateNF": issueDateNF,
            "cnpjIssuer": cnpjIssuer,
            "keyNF": keyNF,
            "statusNF": 1 # cancelada
        }