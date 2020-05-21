import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))
sys.path.append(os.path.join(fileDir, 'backend', 'accounting_integration', 'src'))
sys.path.append(os.path.join(absPath))

import json
from tools.leArquivos import leXls_Xlsx, leTxt, readJson
import tools.funcoesUteis as funcoesUteis
from services.rules.ReturnFilesDontFindForm import ReturnFilesDontFindForm

# arquivos que podem ter ser um pagamento. Ideal depois é ver se consegue abstrair isto pra apenas implementar o modelo
from Transferencia import Transferencia


class ProofsItau(object):

    def __init__(self, wayTemp):
        self._proofs = []
        # possíveis textos que a linha de pagamento começa, exemplo: TRANSFERENCIA REALIZADA EM 19.09.2019
        self._wayTemp = wayTemp
        self._wayTempFilesRead = os.path.join(wayTemp, 'FilesReads.json')

        # deleta os arquivos da pasta temp que já tenham sido processados, pra não processar duas vezes
        returnFilesDontFindForm = ReturnFilesDontFindForm(0, self._wayTemp)
        returnFilesDontFindForm.removeAlreadyProcessed()

    def process(self, file):
        dataFile = leTxt(file, treatAsText=True, removeBlankLines=True)

        valuesOfFile = []

        transferencia = Transferencia(dataFile)
        proofTransferencia = transferencia.process()
        if proofTransferencia is not None:
            valuesOfFile.append(proofTransferencia)

        return valuesOfFile

    def processAll(self):
        for root, dirs, files in os.walk(self._wayTemp):
            for file in files:
                if file.lower().endswith(('.txt')):
                    wayFile = os.path.join(root, file)
                    self._proofs.append(self.process(wayFile))

        return funcoesUteis.removeAnArrayFromWithinAnother(self._proofs)


if __name__ == "__main__":
    proofsPaymentsItau = ProofsItau("C:/programming/baymax/backend/accounting_integration/data/temp/224")
    print(proofsPaymentsItau.processAll())