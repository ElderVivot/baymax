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
from Fgts import Fgts
from Pix import Pix


class ProofsItau(object):

    def __init__(self, wayTemp):
        self._proofs = []
        # possíveis textos que a linha de pagamento começa, exemplo: TRANSFERENCIA REALIZADA EM 19.09.2019
        self._wayTemp = wayTemp
        self._wayTempFilesRead = os.path.join(wayTemp, 'FilesReads.json')

        # deleta os arquivos da pasta temp que já tenham sido processados, pra não processar duas vezes
        returnFilesDontFindForm = ReturnFilesDontFindForm(0, self._wayTemp)
        returnFilesDontFindForm.removeAlreadyProcessed()

    def process(self, file: str):
        dataFile = leTxt(file, treatAsText=True, removeBlankLines=True)
        fileWaySplit = file.split('\\')
        fileWay = '/'.join(fileWaySplit[:len(fileWaySplit)-1])

        defaultSispag = DefaultSispag(dataFile, fileWay)
        proofDefaultSispag = defaultSispag.process()
        if proofDefaultSispag is not None:
            funcoesUteis.updateFilesRead(self._wayTempFilesRead, file.replace('.txt', '.pdf'), 'ProofsPaymentsItau-DefaultSispag')
            return proofDefaultSispag

        transferencia = Transferencia(dataFile, fileWay)
        proofTransferencia = transferencia.process()
        if proofTransferencia is not None:
            funcoesUteis.updateFilesRead(self._wayTempFilesRead, file.replace('.txt', '.pdf'), 'ProofsPaymentsItau-Transferencia')
            return proofTransferencia

        pagamentoBoleto = PagamentoBoleto(dataFile, fileWay)
        proofPagamentoBoleto = pagamentoBoleto.process()
        if proofPagamentoBoleto is not None:
            funcoesUteis.updateFilesRead(self._wayTempFilesRead, file.replace('.txt', '.pdf'), 'ProofsPaymentsItau-PagtoBoleto')
            return proofPagamentoBoleto

        tedC = TedC(dataFile, fileWay)
        proofTedC = tedC.process()
        if proofTedC is not None:
            funcoesUteis.updateFilesRead(self._wayTempFilesRead, file.replace('.txt', '.pdf'), 'ProofsPaymentsItau-TedC')
            return proofTedC

        agendamento = Agendamento(dataFile, fileWay)
        proofAgendamento = agendamento.process()
        if proofAgendamento is not None:
            funcoesUteis.updateFilesRead(self._wayTempFilesRead, file.replace('.txt', '.pdf'), 'ProofsPaymentsItau-Agendamento')
            return proofAgendamento

        darf = Darf(dataFile, fileWay)
        proofDarf = darf.process()
        if proofDarf is not None:
            funcoesUteis.updateFilesRead(self._wayTempFilesRead, file.replace('.txt', '.pdf'), 'ProofsPaymentsItau-Darf')
            return proofDarf

        gps = Gps(dataFile, fileWay)
        proofGps = gps.process()
        if proofGps is not None:
            funcoesUteis.updateFilesRead(self._wayTempFilesRead, file.replace('.txt', '.pdf'), 'ProofsPaymentsItau-Gps')
            return proofGps

        fgts = Fgts(dataFile, fileWay)
        proofFgts = fgts.process()
        if proofFgts is not None:
            funcoesUteis.updateFilesRead(self._wayTempFilesRead, file.replace('.txt', '.pdf'), 'ProofsPaymentsItau-Fgts')
            return proofFgts

        pix = Pix(dataFile, fileWay)
        proofPix = pix.process()
        if proofPix is not None:
            funcoesUteis.updateFilesRead(self._wayTempFilesRead, file.replace('.txt', '.pdf'), 'ProofsPaymentsItau-Pix')
            return proofPix

    def processAll(self):
        for root, _, files in os.walk(self._wayTemp):
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