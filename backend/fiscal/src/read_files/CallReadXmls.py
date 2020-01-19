import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import datetime
from tools.leArquivos import readXml, readJson
import tools.funcoesUteis as funcoesUteis
from fiscal.src.read_files.NFe import NFe
from fiscal.src.read_files.NFeCanceled import NFeCanceled


class CallReadXmls(object):
    def __init__(self, xml):
        self._xml = xml

    def process(self):
        dataXml = readXml(self._xml)

        isNFe = funcoesUteis.returnDataFieldInDict(dataXml, ['nfeProc', 'NFe', 'infNFe', '@Id'])
        isNFeCanceled = funcoesUteis.returnDataFieldInDict(dataXml, ['procEventoNFe', 'evento', 'infEvento', 'chNFe'])
        
        nf = None

        if isNFe != "":
            nfe = NFe(dataXml)
            nf = nfe.readNFe()

        if isNFeCanceled != "":
            nfeCanceled = NFeCanceled(dataXml)
            nf = nfeCanceled.readNFeCanceled()

        return nf