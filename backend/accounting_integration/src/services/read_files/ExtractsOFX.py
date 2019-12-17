import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import json
import codecs
from ofxtools.Parser import OFXTree
from ofxparse import OfxParser
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
            with codecs.open(file) as fileobj:
                ofx = OfxParser.parse(fileobj)

            accountData = ofx.account

            bankId = int(accountData.routing_number)
            bankId = self.returnNameBank(bankId)

            account = accountData.account_id

            transactions = accountData.statement.transactions
            for transaction in transactions:
                typeTransaction = funcoesUteis.treatTextField(transaction.type)
                
                dateTransaction = funcoesUteis.transformaCampoDataParaFormatoBrasileiro(transaction.date)
                
                amount = funcoesUteis.treatDecimalField(transaction.amount)
                if amount < 0:
                    operation = '-'
                    amount *= -1
                else:
                    operation = '+'

                if operation == "+":
                    historicCode = 24
                else:
                    historicCode = 78
                
                document = funcoesUteis.treatTextField(transaction.checknum)

                historic = funcoesUteis.treatTextField(transaction.memo)

                self._valuesOfLine = {
                    "bankId": bankId,
                    "account": account,
                    "typeTransaction": typeTransaction,
                    "dateTransaction": dateTransaction,
                    "amount": amount,
                    "operation": operation,
                    "document": document,
                    "historicCode": historicCode,
                    "historic": historic
                }

                self._valuesOfFile.append(self._valuesOfLine.copy())
        except Exception as e:
            print(e)

        return self._valuesOfFile

# if __name__ == "__main__":
#     extractOFX = ExtractsOFX()
#     extractOFX.process("C:/_temp/integracao_diviart/OUTUBRO CX DIVIART.ofx")
