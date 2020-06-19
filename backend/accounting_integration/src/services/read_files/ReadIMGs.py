import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import json
import shutil
from tools.leArquivos import readJson, ImageToText
import tools.funcoesUteis as funcoesUteis

wayToSaveFiles = open(os.path.join(fileDir, 'backend/accounting_integration/src/WayToSaveFiles.json') )
wayDefault = json.load(wayToSaveFiles)
wayToSaveFiles.close()


class ReadIMGs(object):

    def __init__(self, codiEmp, wayTemp, wayToRead):
        self._codiEmp = codiEmp
        self._wayTemp = wayTemp
        self._wayToRead = wayToRead
        self._pasteIMG = os.path.join(self._wayTemp, "imgs")
        if os.path.exists(self._pasteIMG) is False:
            os.makedirs(self._pasteIMG)
    
    def transformImgToText(self):

        sequential = 0 # este sequencial serve pra caso tenha 2 imgs com mesmo nome em pasta diferentes ele não sobrescreva um ao outro, portanto vai salvar com o nome - sequencial
        
        for root, dirs, files in os.walk(self._wayToRead):
            for file in files:
                if file.lower().endswith(('.jpg', '.png')):
                    sequential += 1
                    wayFile = os.path.join(root, file)
                    basename, _ = os.path.splitext(os.path.basename(wayFile))

                    basename = f'{funcoesUteis.treatTextField(basename)}-{sequential}'
                    
                    ImageToText(wayFile, self._pasteIMG, basename)


if __name__ == "__main__":
    readImgs = ReadIMGs(1073, 'C:/programming/baymax/backend/accounting_integration/data/temp/1073' ,'C:/integracao_contabil/1073/arquivos_originais')
    readImgs.transformImgToText()