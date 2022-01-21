import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import json
import shutil
from tools.leArquivos import leTxt
import tools.funcoesUteis as funcoesUteis


class SanitizeOFX(object):

    def __init__(self, codiEmp, wayToRead, wayTemp):
        self._codiEmp = codiEmp
        self._wayTemp = wayTemp
        self._wayToRead = wayToRead
        self._folderOFX = os.path.join(self._wayTemp, 'ofxs')
        if os.path.exists(self._folderOFX) is False:
            os.makedirs(self._folderOFX)

    def process(self, file, sequential):
        try:
            dataFile = leTxt(file, removeBlankLines=True, treatAsText=True)
            
            nameFile = f"{funcoesUteis.getOnlyNameFile(os.path.basename(file))}-{sequential}.ofx"

            wayFileToSave = os.path.join(self._folderOFX, nameFile)

            with open(wayFileToSave, 'w') as txtfile:
                for row in dataFile:
                    txtfile.write(f'{row}\n')
        except Exception as e:
            print(file, e)
            pass
        
    def processAll(self):
        print('\t - 2.1: Retirando caracteres inválidos OFXs')

        sequential = 0 # este sequencial serve pra caso tenha 2 pdfs com mesmo nome em pasta diferentes ele não sobrescreva um ao outro, portanto vai salvar com o nome - sequencial
        
        for root, dirs, files in os.walk(self._wayToRead):
            for file in files:
                if file.lower().endswith(('.ofx', '.ofc', '.txt')) or file.find('.') < 0:
                    sequential += 1
                    wayFile = os.path.join(root, file)
                    self.process(wayFile, sequential)

                
if __name__ == "__main__":
    codi_emp = str(293)

    extractOFX = SanitizeOFX(codi_emp, f"C:/integracao_contabil/{codi_emp}/arquivos_originais", f"C:/programming/baymax/backend/accounting_integration/data/temp/{codi_emp}")
    extractOFX.processAll()
                    