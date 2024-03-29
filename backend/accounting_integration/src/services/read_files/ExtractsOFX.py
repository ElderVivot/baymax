import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import json
import codecs
import shutil
from ofxparse import OfxParser
from tools.leArquivos import leXls_Xlsx, leTxt, readJson
import tools.funcoesUteis as funcoesUteis
import datetime
from accounting_integration.src.services.read_files.SanitizeOFX import SanitizeOFX


class ExtractsOFX(object):

    def __init__(self, codiEmp, wayOriginal, wayTemp):
        self._extracts = []
        self._codiEmp = codiEmp
        self._wayOriginal = wayOriginal
        self._wayTemp = wayTemp
        self._banks = readJson(os.path.join(fileDir, f'backend/accounting_integration/data/banks.json'))
        # print(self._banks["BanksNamePerNumber"])

        sanitizeOFX = SanitizeOFX(self._codiEmp, self._wayOriginal, self._wayTemp)
        sanitizeOFX.processAll()

    def returnNameBank(self, numberBank):
        try:
            return self._banks["BanksNamePerNumber"][str(numberBank)]
        except Exception:
            return ""

    def returnAccount(self, numberBank, account):
        if numberBank == 748 or numberBank == 341 or numberBank == 3:
            return str(int(account[4:]))
        else:
            return account
    
    def process(self, file, numberFile):

        valuesOfLine = {}
        valuesOfFile = []

        try:
            with codecs.open(file) as fileobj:
                ofx = OfxParser.parse(fileobj, fail_fast=False)

            accountData = ofx.account

            try:
                institution = accountData.institution
                fid = int(institution.fid)
            except Exception:
                fid = 0

            bankId = int(accountData.routing_number)
            bankId = fid if fid == 82 else bankId
            bankName = funcoesUteis.returnBankForNumber(bankId) #self.returnNameBank(bankId)

            account = accountData.account_id
            account = str(account).replace('-', '')
            account = self.returnAccount(bankId, account)

            # shutil.copy(file, f'{self._wayOriginal}/ofx_organizados/{bankName}_{account}_{numberFile}.ofx')

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
                # ignora lancamentos no extrato como saldo parcial, pq nao é um lançamento em si
                if historic == 'SALDO' or historic.find('SALDO PARCIAL') >= 0 or historic.find('SALDO INICIAL') >= 0 \
                    or historic.find('SALDO FINAL') >= 0 or historic.find('SALDO APLIC') >= 0 or historic.find('SALDO A LIBERAR') >= 0 \
                    or historic.find('SDO CTA') >= 0 or historic.find('SALDO') >= 0:
                    continue

                valuesOfLine = {
                    "bank": bankName,
                    "account": account,
                    "typeTransaction": typeTransaction,
                    "dateTransaction": dateTransaction,
                    "amount": round(amount, 2),
                    "operation": operation,
                    "document": document,
                    "historicCode": historicCode,
                    "historic": historic,
                    "wayFile": file
                }

                valuesOfFile.append(valuesOfLine.copy())
        except Exception as e:
            print(file, e)
            pass
        
        return valuesOfFile

    def processAll(self):
        numberFile = 0
        for root, dirs, files in os.walk(self._wayTemp):
            for file in files:
                if file.lower().endswith(('.ofx', '.ofc', '.txt')):
                    numberFile += 1
                    wayFile = os.path.join(root, file)
                    self._extracts.append(self.process(wayFile, numberFile))

        return funcoesUteis.removeAnArrayFromWithinAnother(self._extracts)

if __name__ == "__main__":
    codi_emp = str(3)

    # extractOFX = SanitizeOFX(codi_emp, f"C:/programming/baymax/backend/accounting_integration/data/temp/{codi_emp}", f"C:/integracao_contabil/{codi_emp}/arquivos_originais")
    # extractOFX.processAll()

    extractOFX = ExtractsOFX(codi_emp, f"C:/integracao_contabil/{codi_emp}/arquivos_originais", f"C:/programming/baymax/backend/accounting_integration/data/temp/{codi_emp}")
    print(extractOFX.processAll())
