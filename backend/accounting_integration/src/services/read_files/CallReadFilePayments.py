import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))
sys.path.append(os.path.join(fileDir, 'backend/accounting_integration/src/services/read_files'))

import tools.leArquivos as leArquivos


class CallReadFilePayments(object):
    def __init__(self, system, codiEmp, wayOriginalToRead, wayTemp):
        self._payments = []
        self._system = system
        self._codiEmp = codiEmp
        self._wayOriginalToRead = wayOriginalToRead
        self._wayTemp = wayTemp
        self._waySettings = os.path.join(fileDir, f'backend/accounting_integration/data/settings/company{self._codiEmp}.json')
        self._settings = leArquivos.readJson(self._waySettings)

    def process(self):
        if self._system == 'winthor':
            print('\t - Identificado que o sistema é o winthor, processando leitura dos arquivos')
            from PaymentsWinthor import PaymentsWinthorExcel
            paymentsWinthorExcel = PaymentsWinthorExcel(self._codiEmp, self._wayOriginalToRead, self._wayTemp, self._settings)
            return paymentsWinthorExcel.processAll()

        if self._system == 'faaftech':
            print('\t - Identificado que o sistema é o mesmo da empresa faaftech, processando leitura dos arquivos')
            from PaymentsFaaftech import PaymentsFaaftech
            paymentsFaaftech = PaymentsFaaftech(self._codiEmp, self._wayOriginalToRead, self._wayTemp, self._settings)
            return paymentsFaaftech.processAll()