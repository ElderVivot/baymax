import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import json
import codecs
from ofxparse import OfxParser
from tools.leArquivos import leXls_Xlsx, leTxt, readJson
import tools.funcoesUteis as funcoesUteis
import datetime


class ExtractsOFX(object):

    def __init__(self, wayOriginal):
        self._extracts = []
        self._wayOriginal = wayOriginal
        self._banks = readJson(os.path.join(fileDir, f'backend/accounting_integration/data/banks.json'))
        # print(self._banks["BanksNamePerNumber"])

    def returnNameBank(self, numberBank):
        try:
            return self._banks["BanksNamePerNumber"][str(numberBank)]
        except Exception:
            return ""

    def returnAccount(self, numberBank, account):
        if numberBank == 748 or numberBank == 341:
            return str(int(account[4:]))
        else:
            return account
    
    def process(self, file):

        valuesOfLine = {}
        valuesOfFile = []

        try:
            with codecs.open(file) as fileobj:
                ofx = OfxParser.parse(fileobj, fail_fast=False)

            accountData = ofx.account

            bankId = int(accountData.routing_number)
            bankName = self.returnNameBank(bankId)

            account = accountData.account_id
            account = str(account).replace('-', '')

            transactions = accountData.statement.transactions
            for transaction in transactions:
                typeTransaction = funcoesUteis.treatTextField(transaction.type)
                
                dateTransaction = transaction.date
                dateTransaction = datetime.datetime.date(dateTransaction)
                
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

                valuesOfLine = {
                    "bank": bankName,
                    "account": account,
                    "typeTransaction": typeTransaction,
                    "dateTransaction": dateTransaction,
                    "amount": round(amount, 2),
                    "operation": operation,
                    "document": document,
                    "historicCode": historicCode,
                    "historic": historic
                }

                valuesOfFile.append(valuesOfLine.copy())
        except Exception as e:
            print(e.with_traceback())
        
        return valuesOfFile

    def processAll(self):
        for root, dirs, files in os.walk(self._wayOriginal):
            for file in files:
                if file.lower().endswith(('.ofx', '.ofc', '.txt')):
                    wayFile = os.path.join(root, file)
                    self._extracts.append(self.process(wayFile))

        return funcoesUteis.removeAnArrayFromWithinAnother(self._extracts)

if __name__ == "__main__":
    extractOFX = ExtractsOFX("C:/integracao_contabil/1752/arquivos_originais")
    print(extractOFX.processAll())
