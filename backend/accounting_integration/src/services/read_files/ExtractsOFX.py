import sys
import os

fileDir = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(os.path.join(fileDir, 'backend'))

import json
from ofxtools.Parser import OFXTree
from tools.leArquivos import leXls_Xlsx, leTxt, readJson
import tools.funcoesUteis as funcoesUteis


class ExtractsOFX(object):

    def __init__(self):
        self._valuesOfLine = {}
        self._valuesOfFile = []
        self._banks = readJson(os.path.join(fileDir, f'backend/accounting_integration/data/banks.json'))
        # print(self._banks["BanksNamePerNumber"])

    def returnNameBank(self, numberBank):
        try:
            return self._banks["BanksNamePerNumber"][str(numberBank)]
        except Exception:
            return ""
    
    def process(self, file):

        try:
            parser = OFXTree()

            parser.parse(file)
            ofx = parser.convert()

            bankId = int(ofx.bankmsgsrsv1[0].stmtrs.bankacctfrom.bankid)
            bankId = self.returnNameBank(bankId)

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

                self._valuesOfLine = {
                    "bankId": bankId,
                    "account": account,
                    "typeTransaction": typeTransaction,
                    "dateTransaction": dateTransaction,
                    "amount": amount,
                    "operation": operation,
                    "document": document,
                    "historic": historic
                }

                self._valuesOfFile.append(self._valuesOfLine.copy())
        except Exception as e:
            print(e)

        return self._valuesOfFile

if __name__ == "__main__":
    extractOFX = ExtractsOFX()
    print(extractOFX.process("C:/_temp/integracao_diviart/OUTUBRO CX DIVIART.ofx"))
