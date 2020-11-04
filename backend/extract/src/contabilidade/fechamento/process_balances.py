import os
import sys

absPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(absPath[:absPath.find('extract')])

from calendar import monthrange
from get_balances import GetBalances
from get_has_zeramento import GetHasZeramento
from save_process_db import SaveProcessDb
from tools.funcoesUteis import treatDecimalField

class ProcessBalances():
    def __init__(self, year, month, naturezasConta, companie):
        self._getBalances = GetBalances()
        self._ativo = 0
        self._passivo = 0
        self._receitas = 0
        self._despesas = 0
        self._hasZeramento = False
        self._differenceBetweenAtivoAndPassivo = False
        self._accountResultadoZerado = False
        self._hasPendencia = True
        self._year = year
        self._month = month
        self._naturezasConta = naturezasConta
        self._companie = companie

        self.startAndDate()

    def startAndDate(self):
        last_day_end_date = monthrange(self._year, self._month)[1]  
        self._end_date = f"{self._year}-{self._month:0>2}-{last_day_end_date:0>2}"
        if self._companie['regime_emp'] in (2, 4):
            self._start_date = f"{self._year}-01-01"
        else:
            self._start_date = f"{self._year}-{(self._month-2):0>2}-01"

    def getHasZeramento(self, end_date):
        codi_emp = self._companie['codi_emp']

        self._getZeramento= GetHasZeramento()
        get = self._getZeramento.get(codi_emp, end_date)
        if len(get) > 0:
            self._hasZeramento = True

    def getBalance(self, codi_emp, clas_cta, start_date, end_date):
        get = self._getBalances.get(codi_emp, clas_cta, start_date, end_date)
        credito = treatDecimalField(get[0]['credit'])
        debito = treatDecimalField(get[1]['debit'])
        balance = debito - credito
        balance = round(balance, 2)
        return balance * (-1) if balance < 0 else balance

    def sendToSave(self):
        self._companie['ativo'] = self._ativo
        self._companie['passivo'] = self._passivo
        self._companie['receitas'] = self._receitas
        self._companie['despesas'] = self._despesas
        self._companie['hasZeramento'] = self._hasZeramento
        self._companie['differenceBetweenAtivoAndPassivo'] = self._differenceBetweenAtivoAndPassivo
        self._companie['hasPendencia'] = self._hasPendencia
        self._companie['accountResultadoZerado'] = self._accountResultadoZerado
        self._companie['start_date'] = self._start_date
        self._companie['end_date'] = self._end_date
        self._companie['competence'] = self._end_date[:7]

        self._saveProcessDb = SaveProcessDb(self._companie, 'AccountFechamento')
        self._saveProcessDb.save()

        print(f"- Exportado empresa {self._companie['codi_emp']} - {self._companie['nome_emp']} | mês {self._companie['competence']}")
            
    def process(self):
        self.getHasZeramento(self._end_date)

        for natureza in self._naturezasConta:
            codi_emp = natureza['codi_emp']
            clas_cta = natureza['clas_cta']                      

            if natureza['grupo'] == 'A':
                self._ativo += self.getBalance(codi_emp, clas_cta, self._start_date, self._end_date)
            if natureza['grupo'] == 'P':
                self._passivo += self.getBalance(codi_emp, clas_cta, self._start_date, self._end_date)
            if natureza['grupo'] == 'R' and natureza['natureza'] == 'C':
                self._receitas += self.getBalance(codi_emp, clas_cta, self._start_date, self._end_date)
            if natureza['grupo'] == 'R' and natureza['natureza'] == 'D':
                self._despesas += self.getBalance(codi_emp, clas_cta, self._start_date, self._end_date)

        if self._ativo != self._passivo:
            self._differenceBetweenAtivoAndPassivo = True

        if self._receitas == 0 and self._despesas == 0:
            self._accountResultadoZerado = True

        if self._differenceBetweenAtivoAndPassivo is True or self._accountResultadoZerado is False:
            self._hasPendencia = False

        self.sendToSave()

        self._getBalances.closeConnection()
