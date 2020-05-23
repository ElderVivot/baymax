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
from DefaultSispag import DefaultSispag
from Transferencia import Transferencia
from PagamentoBoleto import PagamentoBoleto
from TedC import TedC
from Agendamento import Agendamento
from Darf import Darf
from Gps import Gps


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

        defaultSispag = DefaultSispag(dataFile)
        proofDefaultSispag = defaultSispag.process()
        if proofDefaultSispag is not None:
            funcoesUteis.updateFilesRead(self._wayTempFilesRead, file.replace('.txt', '.pdf'), 'ProofsPaymentsItau-DefaultSispag')
            return proofDefaultSispag

        transferencia = Transferencia(dataFile)
        proofTransferencia = transferencia.process()
        if proofTransferencia is not None:
            funcoesUteis.updateFilesRead(self._wayTempFilesRead, file.replace('.txt', '.pdf'), 'ProofsPaymentsItau-Transferencia')
            return proofTransferencia

        pagamentoBoleto = PagamentoBoleto(dataFile)
        proofPagamentoBoleto = pagamentoBoleto.process()
        if proofPagamentoBoleto is not None:
            funcoesUteis.updateFilesRead(self._wayTempFilesRead, file.replace('.txt', '.pdf'), 'ProofsPaymentsItau-PagtoBoleto')
            return proofPagamentoBoleto

        tedC = TedC(dataFile)
        proofTedC = tedC.process()
        if proofTedC is not None:
            funcoesUteis.updateFilesRead(self._wayTempFilesRead, file.replace('.txt', '.pdf'), 'ProofsPaymentsItau-TedC')
            return proofTedC

        agendamento = Agendamento(dataFile)
        proofAgendamento = agendamento.process()
        if proofAgendamento is not None:
            funcoesUteis.updateFilesRead(self._wayTempFilesRead, file.replace('.txt', '.pdf'), 'ProofsPaymentsItau-Agendamento')
            return proofAgendamento

        darf = Darf(dataFile)
        proofDarf = darf.process()
        if proofDarf is not None:
            funcoesUteis.updateFilesRead(self._wayTempFilesRead, file.replace('.txt', '.pdf'), 'ProofsPaymentsItau-Darf')
            return proofDarf

        gps = Gps(dataFile)
        proofGps = gps.process()
        if proofGps is not None:
            funcoesUteis.updateFilesRead(self._wayTempFilesRead, file.replace('.txt', '.pdf'), 'ProofsPaymentsItau-Gps')
            return proofGps

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
    proofsPaymentsItau = ProofsItau("C:/programming/baymax/backend/accounting_integration/data/temp/1657/pdfs/teste")
    print(proofsPaymentsItau.processAll())