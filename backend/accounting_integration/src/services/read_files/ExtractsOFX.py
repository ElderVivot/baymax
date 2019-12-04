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
        self._valuesOfLine = {}
        self._valuesOfFile = []

    def process(self, file):

        try:
            parser = OFXTree()

            parser.parse(file)
            ofx = parser.convert()

            bankId = ofx.bankmsgsrsv1[0].stmtrs.bankacctfrom.bankid
            account = ofx.bankmsgsrsv1[0].stmtrs.bankacctfrom.acctid

            transactions = ofx.bankmsgsrsv1[0].stmtrs.banktranlist
            for transction in transactions:
                typeTransaction = funcoesUteis.treatTextField(transction.trntype)
                
                dateTransaction = funcoesUteis.transformaCampoDataParaFormatoBrasileiro(transction.dtposted)
                
                amount = funcoesUteis.treatDecimalField(transction.trnamt)
                if amount < 0:
                    operation = '-'
                    amount *= -1
                else:
                    operation = '+'
                
                document = funcoesUteis.treatTextField(transction.checknum)

                historic = funcoesUteis.treatTextField(transction.memo)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    extractOFX = ExtractsOFX()
    extractOFX.process("C:/_temp/integracao_diviart/Extrato Conta Corrente-44388-9.ofx")
