import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(absPath[:absPath.find('accounting_integration')])

import json
from tools.leArquivos import leXls_Xlsx, leTxt, readJson
import tools.funcoesUteis as funcoesUteis
from accounting_integration.src.services.rules.ReturnFilesDontFindForm import ReturnFilesDontFindForm

# arquivos que podem ter ser um pagamento. Ideal depois é ver se consegue abstrair isto pra apenas implementar o modelo
from accounting_integration.src.services.read_files.ProofsSicoob.Pagamento import Pagamento


class ProofsSicoob(object):

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

        fileWaySplit = file.split('\\')
        fileWay = '/'.join(fileWaySplit[:len(fileWaySplit)-1])

        pagamento = Pagamento(dataFile, fileWay)
        proofPagamento = pagamento.process()
        if proofPagamento is not None:
            funcoesUteis.updateFilesRead(self._wayTempFilesRead, file.replace('.txt', '.pdf'), 'ProofsPaymentsSicoob-Pagamento')
            return proofPagamento

    def processAll(self):
        for root, dirs, files in os.walk(self._wayTemp):
            for file in files:
                if file.lower().endswith(('.txt')):
                    wayFile = os.path.join(root, file)
                    resultProcess = self.process(wayFile)
                    if resultProcess is not None:
                        self._proofs.append(resultProcess)

        self._proofs = funcoesUteis.removeAnArrayFromWithinAnother(self._proofs)
        return self._proofs


if __name__ == "__main__":
    proofs = ProofsSicoob("C:/programming/baymax/backend/accounting_integration/data/temp/81/pdfs")
    print(len(proofs.processAll()))