from get_natureza_conta import GetNaturezaConta
from process_balances import ProcessBalances

class ProcessNaturezaConta():
    def __init__(self, year, month, companies):
        self._year = year
        self._month = month
        self._companies = companies

    def process(self):
        for companie in self._companies:
            if companie['regime_emp'] in (2, 4) and self._month in (3, 6, 9):
                continue
            
            getNaturezaConta = GetNaturezaConta(companie['codi_emp'])
            naturezaConta = getNaturezaConta.get()

            processBalances = ProcessBalances(self._year, self._month, naturezaConta, companie)
            processBalances.process()
