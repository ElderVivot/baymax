import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import json
import shutil
from tools.leArquivos import readJson
import tools.funcoesUteis as funcoesUteis

wayToSaveFiles = open(os.path.join(fileDir, 'backend/accounting_integration/src/WayToSaveFiles.json') )
wayDefault = json.load(wayToSaveFiles)
wayToSaveFiles.close()


class ReturnFilesDontFindForm(object):

    def __init__(self, codiEmp, wayTemp):
        self._codiEmp = codiEmp
        self._wayTemp = wayTemp
        self._wayTempFilesRead = os.path.join(wayTemp, 'FilesReads.json')
        self._filesRead = readJson(self._wayTempFilesRead)
        self._wayBaseToSaveFiles = os.path.join(wayDefault['WayToSaveFilesOriginals'], f'{self._codiEmp}/arquivos_processados/docs_nao_lidos')
        if os.path.exists(self._wayBaseToSaveFiles) is False:
            os.makedirs(self._wayBaseToSaveFiles)

    def processAll(self):
        for root, dirs, files in os.walk(self._wayTemp):
            for file in files:
                if file.lower().endswith(('.pdf')):
                    wayFile = os.path.join(root, file)
                    wayFileName = wayFile.replace('/', '\\')
                    if funcoesUteis.analyzeIfFieldIsValid(self._filesRead, wayFileName) == "":

                        nameFileOriginal = root.split('\\')[-1]
                        wayToSave = os.path.join(self._wayBaseToSaveFiles, nameFileOriginal)
                        if os.path.exists(wayToSave) is False:
                            os.makedirs(wayToSave)
                            
                        shutil.copy(wayFile, os.path.join(wayToSave, file))

# if __name__ == "__main__":
#     returnFilesDontFindForm = ReturnFilesDontFindForm(890, 'C:/Programming/baymax/backend/accounting_integration/data/temp/890')
#     returnFilesDontFindForm.processAll()