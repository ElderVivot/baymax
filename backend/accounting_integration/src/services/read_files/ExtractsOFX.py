import sys
import os

fileDir = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(os.path.join(fileDir, 'backend'))

import json
from ofxtools.Parser import OFXTree
from tools.leArquivos import leXls_Xlsx, leTxt
import tools.funcoesUteis as funcoesUteis


class ExtractsOFX(object):

    def __init__(self):
        self._extracts = []

    def process(self, file):

        parser = OFXTree()

        parser.parse(file)
        ofx = parser.convert()

        transactions = ofx.bankmsgsrsv1[0].stmtrs.banktranlist
        for transction in transactions:
            print(transction)

        # tx = ofx.invstmtmsgsrsv1[0].invstmtrs.invtranlist[-1]

if __name__ == "__main__":
    extractOFX = ExtractsOFX()
    extractOFX.process("C:/_temp/integracao_diviart/extratonuclear092019.ofx")
