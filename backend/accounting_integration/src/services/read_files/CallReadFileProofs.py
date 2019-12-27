import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))
sys.path.append(os.path.join(fileDir, 'backend/accounting_integration/src/services/read_files'))

import tools.leArquivos as leArquivos
import tools.funcoesUteis as funcoesUteis
from read_files.ProofsPaymentsItau import ProofsPaymentsItau, SispagItauExcel
from read_files.ProofsPaymentsSantander import ProofsPaymentsSantander


class CallReadFileProofs(object):
    def __init__(self, codiEmp, wayTemp):
        self._proofs = []
        self._codiEmp = codiEmp
        self._wayTemp = wayTemp
        self._waySettings = os.path.join(fileDir, f'backend/accounting_integration/data/settings/company{self._codiEmp}.json')
        self._settings = leArquivos.readJson(self._waySettings)

    def process(self):
        try:
            banksList = self._settings["banks"]["listNumbers"]
        except Exception:
            banksList = [0]

        if banksList.count(341) > 0:
            print(f'\t - Processando comprovantes de pagamento do Itaú')
            proofsPaymentsItau = ProofsPaymentsItau(self._wayTemp)
            self._proofs.append(proofsPaymentsItau.processAll())
        
        if banksList.count(33) > 0:
            print(f'\t - Processando comprovantes de pagamento do Santander')
            proofsPaymentsSantander = ProofsPaymentsSantander(self._wayTemp)
            self._proofs.append(proofsPaymentsSantander.processAll())

        return funcoesUteis.removeAnArrayFromWithinAnother(self._proofs)