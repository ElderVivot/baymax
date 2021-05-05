import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import json
import shutil
from tools.leArquivos import leTxt
import tools.funcoesUteis as funcoesUteis

wayToSaveFiles = open(os.path.join(fileDir, 'backend/accounting_integration/src/WayToSaveFiles.json') )
wayDefault = json.load(wayToSaveFiles)
wayToSaveFiles.close()


class SanitizeOFX(object):

    def __init__(self, codiEmp, wayToRead, wayTemp):
        self._codiEmp = codiEmp
        self._wayTemp = wayTemp
        self._wayToRead = wayToRead
        self._folderOFX = os.path.join(self._wayTemp, 'ofxs')
        if os.path.exists(self._folderOFX) is False:
            os.makedirs(self._folderOFX)

    def process(self, file, sequential):
        dataFile = leTxt(file, removeBlankLines=True, treatAsText=True)

        dateExtract = None
        historic = None
        amount = 0
        balance = 0
        document = ''

        extractsTemp = []
        extracts = []

        for data in dataFile:
            dataSplit = data.split(' ')
            dateExtract = funcoesUteis.treatDateFieldInVector(dataSplit, 1)
            document = funcoesUteis.treatTextFieldInVector(dataSplit, -3)
            amount = funcoesUteis.treatDecimalFieldInVector(dataSplit, -2)
            balance = funcoesUteis.treatDecimalFieldInVector(dataSplit, -1)

            historic = ' '.join(dataSplit[1:len(dataSplit)-4])
            historic = funcoesUteis.treatTextField(historic)

            if dateExtract is not None and amount > 0:
                extractsTemp.append({
                    "dateExtract": dateExtract,
                    "document": document,
                    "amount": amount,
                    "balance": balance,
                    "historic": historic
                })

        for key, extract in enumerate(extractsTemp):
            if key > 0:
                beforeExtract = extractsTemp[key-1]

                balanceBefore = beforeExtract['balance']
                balanceActual = extract['balance']
                if balanceBefore > balanceActual:
                    extract['operation'] = '-'
                else:
                    extract['operation'] = '+'
            else:
                extract['operation'] = '+'

            dataFormatada = funcoesUteis.transformaCampoDataParaFormatoBrasileiro(extract['dateExtract'])
            print(f"{dataFormatada};{extract['document']};{extract['historic']};{extract['operation']}{extract['amount']:.2f};{extract['operation']};SANTANDER;0971130017960")

        
        # nameFile = f"{funcoesUteis.getOnlyNameFile(os.path.basename(file))}-{sequential}.ofx"

        # wayFileToSave = os.path.join(self._folderOFX, nameFile)

        # with open(wayFileToSave, 'w') as txtfile:
        #     for row in dataFile:
        #         txtfile.write(f'{row}\n')
        
    def processAll(self):
        print('- Processando extrato protheus')

        sequential = 0 # este sequencial serve pra caso tenha 2 pdfs com mesmo nome em pasta diferentes ele não sobrescreva um ao outro, portanto vai salvar com o nome - sequencial
        
        for root, dirs, files in os.walk(self._wayToRead):
            for file in files:
                if file.lower().endswith(('.txt')):
                    sequential += 1
                    wayFile = os.path.join(root, file)
                    self.process(wayFile, sequential)

                
if __name__ == "__main__":
    codi_emp = str(1822)

    extractOFX = SanitizeOFX(codi_emp, f"C:/integracao_contabil/{codi_emp}/arquivos_originais", f"C:/programming/baymax/backend/accounting_integration/data/temp/{codi_emp}")
    extractOFX.processAll()