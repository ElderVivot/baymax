import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))
sys.path.append(os.path.join(fileDir, 'backend/accounting_integration/src/services/read_files'))

import tools.leArquivos as leArquivos
import tools.funcoesUteis as funcoesUteis


class CallReadFileProofs(object):
    def __init__(self, codiEmp, wayTemp, wayOriginal, banksList):
        self._proofs = []
        self._codiEmp = codiEmp
        self._wayTemp = wayTemp
        self._wayOriginal = wayOriginal
        self._banksList = banksList

    def process(self):        
        if self._banksList.count(341) > 0:
            print(f'\t - Processando comprovantes de pagamento do Itaú')
            from read_files.ProofsPaymentsItau import ProofsPaymentsItau, SispagItauExcel

            try:
                isSispagExcel = self._settings["proofsPayments"]["341"]["model"]
            except Exception:
                isSispagExcel = None

            if isSispagExcel is not None:
                proofsPaymentsItau = SispagItauExcel(self._wayOriginal)
            else: 
                proofsPaymentsItau = ProofsPaymentsItau(self._wayTemp)
                
            self._proofs.append(proofsPaymentsItau.processAll())
        
        if self._banksList.count(33) > 0:
            print(f'\t - Processando comprovantes de pagamento do Santander')
            from read_files.ProofsPaymentsSantander import ProofsPaymentsSantander
            proofsPaymentsSantander = ProofsPaymentsSantander(self._wayTemp)
            self._proofs.append(proofsPaymentsSantander.processAll())

        return funcoesUteis.removeAnArrayFromWithinAnother(self._proofs)