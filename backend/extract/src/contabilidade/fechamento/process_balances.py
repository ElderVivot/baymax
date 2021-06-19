import os
import sys

absPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(absPath[:absPath.find('extract')])

from calendar import monthrange
from get_balances import GetBalances
from get_balances_period import GetBalancesPeriod
from get_has_zeramento import GetHasZeramento
from save_process_db import SaveProcessDb
from tools.funcoesUteis import treatDecimalField, retornaCampoComoData

class ProcessBalances():
    def __init__(self, year, month, naturezasConta, companie):
        self._getBalances = GetBalances()
        self._getBalancesPeriod = GetBalancesPeriod()
        self._ativo = 0
        self._passivo = 0
        self._receitas = 0
        self._despesas = 0
        self._hasZeramento = False
        self._differenceBetweenAtivoAndPassivo = False
        self._accountResultadoZerado = False
        self._hasFechamentoCompleto = False
        self._year = year
        self._month = month
        self._naturezasConta = naturezasConta
        self._companie = companie
        self._amountResultado = 0
        self._codi_emp = self._companie['codi_emp']
        self._codi_emp_plano_contas = self._codi_emp if self._companie['codi_emp_plano_contas'] is None else self._companie['codi_emp_plano_contas']
        
        self.startAndDate()

    def startAndDate(self):
        last_day_end_date = monthrange(self._year, self._month)[1]  
        self._end_date = f"{self._year}-{self._month:0>2}-{last_day_end_date:0>2}"
        self._competence = self._end_date[:7]
        
        if self._companie['regime_emp'] in (2, 4):
            self._start_date = f"{self._year}-01-01"
        else:
            self._start_date = f"{self._year}-{(self._month-2):0>2}-01"

        if self._companie['dina_emp'] is not None:            
            dina_emp = retornaCampoComoData(self._companie['dina_emp'][:10], formatoData=2)
            year_dina_emp = dina_emp.year
            month_dina_emp = dina_emp.month

            start_date = retornaCampoComoData(self._start_date, formatoData=2)
            end_date = retornaCampoComoData(self._end_date, formatoData=2)
            if start_date <= dina_emp and dina_emp <= end_date:                
                last_day_end_date = monthrange(year_dina_emp, month_dina_emp)[1]  
                self._end_date = f"{year_dina_emp}-{month_dina_emp:0>2}-{last_day_end_date:0>2}"

    def getHasZeramento(self, end_date):
        self._getZeramento= GetHasZeramento()
        get = self._getZeramento.get(self._codi_emp, end_date)
        if len(get) > 0:
            self._hasZeramento = True

    def getBalance(self, clas_cta):
        get = self._getBalances.get(self._codi_emp, self._codi_emp_plano_contas, clas_cta, self._start_date, self._end_date)
        credito = treatDecimalField(get[0]['credit'])
        debito = treatDecimalField(get[1]['debit'])
        balance = debito - credito
        balance = round(balance, 2)
        return balance * (-1) if balance < 0 else balance

    def getBalancePeriod(self, clas_cta, accountResultado):
        get = self._getBalancesPeriod.get(self._codi_emp, self._codi_emp_plano_contas, clas_cta, self._start_date, self._end_date)
        credito = treatDecimalField(get[0]['credit'])
        debito = treatDecimalField(get[1]['debit'])
        if accountResultado is True:
            self._amountResultado += debito + credito

    def sendToSave(self):
        self._companie['ativo'] = self._ativo
        self._companie['passivo'] = self._passivo
        self._companie['receitas'] = self._receitas
        self._companie['despesas'] = self._despesas
        self._companie['amountResultado'] = self._amountResultado
        self._companie['hasZeramento'] = self._hasZeramento
        self._companie['differenceBetweenAtivoAndPassivo'] = self._differenceBetweenAtivoAndPassivo
        self._companie['hasFechamentoCompleto'] = self._hasFechamentoCompleto
        self._companie['accountResultadoZerado'] = self._accountResultadoZerado
        self._companie['start_date'] = self._start_date
        self._companie['end_date'] = self._end_date
        self._companie['competence'] = self._competence

        self._saveProcessDb = SaveProcessDb(self._companie, 'AccountFechamento')
        self._saveProcessDb.save()

        print(f"- Exportado empresa {self._codi_emp} - {self._companie['nome_emp']} | período {self._companie['start_date']} à {self._companie['end_date']}")
            
    def process(self):
        self.getHasZeramento(self._end_date)

        for natureza in self._naturezasConta:
            clas_cta = natureza['clas_cta']                      

            if natureza['grupo'] == 'A':
                self._ativo += self.getBalance(clas_cta)
            if natureza['grupo'] == 'P':
                self._passivo += self.getBalance(clas_cta)
            if natureza['grupo'] == 'R' and natureza['natureza'] == 'C':
                self._receitas += self.getBalance(clas_cta)
                self.getBalancePeriod(clas_cta, accountResultado=True)
            if natureza['grupo'] == 'R' and natureza['natureza'] == 'D':
                self._despesas += self.getBalance(clas_cta)
                self.getBalancePeriod(clas_cta, accountResultado=True)

        if self._ativo != self._passivo:
            self._differenceBetweenAtivoAndPassivo = True

        if self._receitas == 0 and self._despesas == 0:
            self._accountResultadoZerado = True

        if self._amountResultado == 0:
            self._hasZeramento = True

        if self._differenceBetweenAtivoAndPassivo is False and self._accountResultadoZerado is True and self._hasZeramento is True:
            self._hasFechamentoCompleto = True

        self.sendToSave()

        self._getBalances.closeConnection()
