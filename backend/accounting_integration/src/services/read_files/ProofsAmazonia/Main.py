import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(absPath[:absPath.find('accounting_integration')])

import json
from tools.leArquivos import leXls_Xlsx, leTxt, readJson
import tools.funcoesUteis as funcoesUteis
from accounting_integration.src.services.rules.ReturnFilesDontFindForm import ReturnFilesDontFindForm

# arquivos que podem ter ser um pagamento. Ideal depois é ver se consegue abstrair isto pra apenas implementar o modelo
from accounting_integration.src.services.read_files.ProofsAmazonia.Transferencia import Transferencia
from accounting_integration.src.services.read_files.ProofsAmazonia.Pagamento import Pagamento
from accounting_integration.src.services.read_files.ProofsAmazonia.PagamentoConvenio import PagamentoConvenio
from accounting_integration.src.services.read_files.ProofsAmazonia.PagamentoInss import PagamentoInss


class ProofsAmazonia(object):

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

        transferencia = Transferencia(dataFile)
        proofTransferencia = transferencia.process()
        if proofTransferencia is not None:
            funcoesUteis.updateFilesRead(self._wayTempFilesRead, file.replace('.txt', '.pdf'), 'ProofsPaymentsAmazonia-Transferencia')
            return proofTransferencia

        pagamento = Pagamento(dataFile)
        proofPagamento = pagamento.process()
        if proofPagamento is not None:
            funcoesUteis.updateFilesRead(self._wayTempFilesRead, file.replace('.txt', '.pdf'), 'ProofsPaymentsAmazonia-Pagamento')
            return proofPagamento

        pagamentoConvenio = PagamentoConvenio(dataFile)
        proofPagamentoConvenio = pagamentoConvenio.process()
        if proofPagamentoConvenio is not None:
            funcoesUteis.updateFilesRead(self._wayTempFilesRead, file.replace('.txt', '.pdf'), 'ProofsPaymentsAmazonia-PagamentoConvenio')
            return proofPagamentoConvenio

        pagamentoInss = PagamentoInss(dataFile)
        proofPagamentoInss = pagamentoInss.process()
        if proofPagamentoInss is not None:
            funcoesUteis.updateFilesRead(self._wayTempFilesRead, file.replace('.txt', '.pdf'), 'ProofsPaymentsAmazonia-PagamentoInss')
            return proofPagamentoInss

    def processAll(self):
        for root, dirs, files in os.walk(self._wayTemp):
            for file in files:
                if file.lower().endswith(('.txt')):
                    wayFile = os.path.join(root, file)
                    resultProcess = self.process(wayFile)
                    if resultProcess is not None:
                        self._proofs.append(resultProcess)

        return self._proofs


if __name__ == "__main__":
    proofs = ProofsAmazonia("C:/programming/baymax/backend/accounting_integration/data/temp/1518/pdfs")
    print(proofs.processAll())