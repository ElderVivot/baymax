import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import tools.funcoesUteis as funcoesUteis


class FilterPeriod(object):

    def __init__(self, inicialDate, finalDate, payments=[], extracts=[]):
        self._payments = payments
        self._extracts = extracts
        self._paymentsWithFilter = []
        self._extractsWithFilter = []
        self._inicialDate = funcoesUteis.retornaCampoComoData(inicialDate)
        self._finalDate = funcoesUteis.retornaCampoComoData(finalDate)

    def filterPayments(self):
        for payment in self._payments:
            paymentDate = funcoesUteis.analyzeIfFieldIsValid(payment, "paymentDate", None)
            extractDate = funcoesUteis.analyzeIfFieldIsValid(payment, "dateExtract", None)
            if extractDate is None or extractDate == "":
                extractDate = paymentDate

            if ( self._inicialDate <= paymentDate and paymentDate <= self._finalDate ) or ( self._inicialDate <= extractDate and extractDate <= self._finalDate ):
                self._paymentsWithFilter.append(payment)

        return self._paymentsWithFilter

    def filterExtracts(self):
        for extract in self._extracts:
            extractDate = funcoesUteis.analyzeIfFieldIsValid(extract, "dateTransaction", None)

            if self._inicialDate <= extractDate and extractDate <= self._finalDate:
                self._extractsWithFilter.append(extract)

        return self._extractsWithFilter         

