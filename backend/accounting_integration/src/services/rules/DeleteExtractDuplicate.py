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

    def checkIfDuplicate(self, extract) -> bool:
        qtdExtract = list(filter(lambda x: x == extract, self._extractsWithOnlyDataNecessary))
        return False if len(qtdExtract) < 1 else True

    def process(self):
        for extract in self._extracts:
            newExtract = self.cleanExtractWithOnlyDataNecessary(extract.copy())
            duplicateExtract = self.checkIfDuplicate(newExtract)
            if duplicateExtract is not True:
                self._extractsWithOnlyDataNecessary.append(newExtract)
                self._newExtracts.append(extract)
            else:
                continue

        return self._newExtracts

