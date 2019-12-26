import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))
sys.path.append(os.path.join(fileDir, 'backend/accounting_integration/src/services'))

import json
from tools.leArquivos import leXls_Xlsx, leTxt, readJson
import tools.funcoesUteis as funcoesUteis
from rules.ReturnFilesDontFindForm import ReturnFilesDontFindForm


class ProofsPaymentsSantander(object):

    def __init__(self, wayTemp):
        self._proofs = []
        self._wayTemp = wayTemp
        self._wayTempFilesRead = os.path.join(wayTemp, 'FilesReads.json')
        self._beneficiaryOrPayer = ''

        # deleta os arquivos da pasta temp que já tenham sido processados, pra não processar duas vezes
        returnFilesDontFindForm = ReturnFilesDontFindForm(0, self._wayTemp)
        returnFilesDontFindForm.removeAlreadyProcessed()

    def isProof(self, file):
        dataFile = leTxt(file, treatAsText=True, removeBlankLines=True)
        countProof = 0
        for data in dataFile:
            data = funcoesUteis.treatTextField(data)

            if data.find('CENTRAL DE ATENDIMENTO SANTANDER EMPRESARIAL') >= 0:
                countProof += 1
            if ( data.find('4004') >= 0 or data.find('726') ) and data.find('2125') >= 0:
                countProof += 1
            
            if countProof == 3:
                return True

    def process(self, file):
        # se não for desta classe nem segue pra frente
        if self.isProof(file) is None:
            return []

        funcoesUteis.updateFilesRead(self._wayTempFilesRead, file.replace('.txt', '.pdf'), 'ProofsPaymentsSantander')
        
        valuesOfLine = {}
        valuesOfFile = []

        dataFile = leTxt(file, treatAsText=True, removeBlankLines=True)

        nameProvider = ""
        historic = ""
        dueDate = None
        paymentDate = None
        company = ""
        cnpjProvider = ""
        amountPaid = float(0)
        amountOriginal = float(0)
        amountInterest = float(0)
        category = ""
        bank = "SANTANDER"
        account = ""

        for data in dataFile:

            data = str(data)
            dataSplit = data.split(':')

            fieldOne = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 1))

            fieldTwo = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 2))

            if data.find('CONTA CORRENTE:') >= 0:
                account = data[ data.find('CONTA CORRENTE:') + 15: ]
                account = funcoesUteis.treatTextField(account)
                accountSplit = account.split('-') 
                account = f"{funcoesUteis.analyzeIfFieldIsValidMatrix(accountSplit, 1)}{funcoesUteis.analyzeIfFieldIsValidMatrix(accountSplit, 2)}"

            if data.find('BENEFICIARIO ORIGINAL') >= 0:
                self._beneficiaryOrPayer = 'BENEFICIARIO'
            elif data.count('PAGADOR ORIGINAL') > 0:
                self._beneficiaryOrPayer = 'PAGADOR'

            if self._beneficiaryOrPayer == 'PAGADOR':
                pass
                    
            elif self._beneficiaryOrPayer == 'BENEFICIARIO':
                if fieldOne == "RAZAO SOCIAL":
                    nameProvider = fieldTwo.replace('RAZAO SOCIAL', '')

                if fieldOne == "CNPJ":
                    cnpjProvider = fieldTwo.replace('CNPJ', '')

            if fieldOne == "DATA DE VENCIMENTO":
                dueDate = funcoesUteis.transformaCampoDataParaFormatoBrasileiro(funcoesUteis.retornaCampoComoData(fieldTwo))

            if fieldOne.count("VALOR NOMINAL") > 0:
                amountOriginal = funcoesUteis.treatDecimalField(fieldTwo)

            if fieldOne.count("ENCARGOS") > 0:
                amountInterest = funcoesUteis.treatDecimalField(fieldTwo)

            if fieldOne.count("TOTAL A COBRAR") > 0:
                amountPaid = funcoesUteis.treatDecimalField(fieldTwo)

            if amountInterest > 0:
                amountOriginal = amountPaid - amountInterest # é necessário fazer pois as vezes tem juros mas o valor nominal tá igual ao valor pago
            else:
                amountInterest = amountPaid - amountOriginal # é necessário fazer  pois as vezes tem juros, mas não tem o campo encargos

            if fieldOne == "DATA DA TRANSACAO":
                paymentDate = funcoesUteis.retornaCampoComoData(fieldTwo)

            if paymentDate is not None and amountPaid > 0:
                valuesOfLine = {
                    "paymentDate": funcoesUteis.transformaCampoDataParaFormatoBrasileiro(paymentDate),
                    "nameProvider": nameProvider,
                    "cnpjProvider": cnpjProvider,
                    "dueDate": dueDate,
                    "bank": bank,
                    "account": account,
                    "amountPaid": amountPaid,
                    "amountDiscount": float(0),
                    "amountInterest": amountInterest,
                    "amountOriginal": amountOriginal,
                    "historic": historic,
                    "category": category,
                    "company": company,
                    "foundProof": True
                }

                valuesOfFile.append(valuesOfLine.copy())

                paymentDate = None
                amountPaid = float(0)

        return valuesOfFile

    def processAll(self):
        for root, dirs, files in os.walk(self._wayTemp):
            for file in files:
                if file.lower().endswith(('.txt')):
                    wayFile = os.path.join(root, file)
                    self._proofs.append(self.process(wayFile))

        return funcoesUteis.removeAnArrayFromWithinAnother(self._proofs)

# if __name__ == "__main__":
#     proofs = ProofsPaymentsSantander("C:/programming/baymax/backend/accounting_integration/data/temp/1751")
#     print(proofs.process("C:/programming/baymax/backend/accounting_integration/data/temp/1751/pdfs/santander01a15102019-3/1.txt"))
            