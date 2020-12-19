import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import tools.funcoesUteis as funcoesUteis


class DeleteExtractDuplicate(object):

    def __init__(self, extracts=[]):
        self._extracts = extracts
        self._newExtracts = []
        self._extractsWithOnlyDataNecessary = []

    def cleanExtractWithOnlyDataNecessary(self, extract):
        del extract['historicCode']
        del extract['historic']
        document = funcoesUteis.analyzeIfFieldIsValid(extract, "document", None)
        document = funcoesUteis.treatNumberField(document, isInt=True)
        extract['document'] = document
        return extract
    
    # def extractWithOnlyDataNecessary(self):
    #     for extract in self._extracts:
    #         newExtract = self.cleanExtractWithOnlyDataNecessary(extract)
    #         self._extractsWithOnlyDataNecessary.append(newExtract)

    def checkIfDuplicate(self, extract) -> bool:
        qtdExtract = list(filter(lambda x: x == extract, self._newExtracts))
        return False if len(qtdExtract) < 1 else True

    def process(self):
        # self.extractWithOnlyDataNecessary()
        for extract in self._extracts:
            newExtract = self.cleanExtractWithOnlyDataNecessary(extract)
            duplicateExtract = self.checkIfDuplicate(newExtract)
            if duplicateExtract is not True:
                self._newExtracts.append(newExtract)
            else:
                continue

        return self._newExtracts

