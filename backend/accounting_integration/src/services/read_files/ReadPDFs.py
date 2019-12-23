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


class ReadPDFs(object):

    def __init__(self, codiEmp, wayTemp):
        self._codiEmp = codiEmp
        self._wayTemp = wayTemp
        
    def processAll(self):
        for root, dirs, files in os.walk(self._wayTemp):
            for file in files:
                if file.lower().endswith(('.pdf')):
                    wayFile = os.path.join(root, file)