import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))
sys.path.append(os.path.join(fileDir, 'backend/accounting_integration/src/services'))

import json
from datetime import datetime, timedelta
from tools.leArquivos import leXls_Xlsx, leTxt
import tools.funcoesUteis as funcoesUteis


class ComparePaymentsAndProofWithExtracts(object):

    def __init__(self, settings, extracts=[], payments=[], proofOfPayments=[]):
        self._settings = settings
        self._extracts = extracts
        self._payments = payments
        self._proofOfPayments = proofOfPayments
        self._paymentsFinal = []
        self._paymentsAlreadyRead = []
        self._extractsExistsInPayments = [] # este daqui são para os extratos que encontrou correlação nos pagamentos, na planilha de extratos conterá um campo com esta informação
        self._extractsToSearch = self._extracts.copy() # este daqui é que vai ser utilizado pra procurar se o pagamento existe correspondente no extrato, conforme for encontrando vai excluindo pra não procurar novamente num que já tinha retornado
        self._paymentsToSearch = self._payments.copy() # este daqui é que vai ser utilizado pra procurar se o pagamento existe correspondente no comprovante de pagamento, conforme for encontrando vai excluindo pra não procurar novamente num que já tinha retornado
        self._extractsFinal = []
        self._numberOfDaysInterval = 3
        self._numberOfDaysIntervalPaymentWithProof = 3
        self._financyIsReliable = funcoesUteis.returnDataFieldInDict(self._settings, ['financy', 'isReliable'], True)

    def findsLessDifferenceBetweenDatesInArrayOfObject(self, arrayObjects, nameFieldOfDate, baseDate):
        objReturn = None
        smallerDifferenceBetweenDates = None

        for obj in arrayObjects:
            objDate = obj[nameFieldOfDate]

            differenceBetweenDates = abs((baseDate - objDate).days)

            # se a diferença entre datas for zero, nem segue a pesquisa, pois já retorno a data correta
            if differenceBetweenDates == 0:
                objReturn = obj
                break

            if smallerDifferenceBetweenDates is None:
                smallerDifferenceBetweenDates = differenceBetweenDates
                objReturn = obj

            if differenceBetweenDates < smallerDifferenceBetweenDates:
                smallerDifferenceBetweenDates = differenceBetweenDates
                objReturn = obj

        return objReturn

    def returnDayFoundInPayment(self, payment, paymentDate, amountPaid, bank, account, typeComparation):
        # :typeComparation --> 1 = completa (banco e conta corrente); 2 = média (banco); 3 = fraca (apenas valores, data e operação)
        datePayment = payment['paymentDate']
        amountPayment = payment['amountPaid']
        bankPayment = payment['bank']
        accountPayment = payment['account']
        search = False

        # caso o valor seja diferente nem processa os dias
        if amountPayment != amountPaid:
            return search

        # caso a diferença entre as datas seja maior que o intervalo definido já retorna falso
        differenceBetweenDates = abs((paymentDate - datePayment).days)
        if differenceBetweenDates > self._numberOfDaysIntervalPaymentWithProof:
            return search

        # procura nos dias positivos e negativos (da data atual até mais 3 dias pra frente/atrás)
        for day in range(0, self._numberOfDaysIntervalPaymentWithProof+1):
            paymentDateComparison = paymentDate + timedelta(days=day)
            paymentDateComparisonLess = paymentDate + timedelta(days=-day)
            if typeComparation == 1:
                if ( datePayment == paymentDateComparison or datePayment == paymentDateComparisonLess ) and amountPayment == amountPaid and bankPayment.find(bank) >= 0 and accountPayment.find(account) >= 0:
                    search = True
                    break
            elif typeComparation == 2:
                if ( datePayment == paymentDateComparison or datePayment == paymentDateComparisonLess ) and amountPayment == amountPaid and bankPayment.find(bank) >= 0:
                    search = True
                    break
            elif typeComparation == 3:
                if ( datePayment == paymentDateComparison or datePayment == paymentDateComparisonLess ) and amountPayment == amountPaid:
                    search = True
                    break

        return search        

    def returnDataPayment(self, paymentDate, amountPaid, bank='', account=''):  
        # o range de 1 a 3 é pq primeiro vou rodar o typeComparation com mais confiabilidade (igual a 1), depois rodo com média e fraca por último
        for numberSequencial in range(1, 4):
            paymentsFound = []
            paymentReturn = None

            for payment in self._paymentsToSearch:
                search = self.returnDayFoundInPayment(payment, paymentDate, amountPaid, bank, account, typeComparation=numberSequencial)
                if search is True:
                    paymentsFound.append(payment)
            
            if len(paymentsFound) > 0:
                paymentReturn = self.findsLessDifferenceBetweenDatesInArrayOfObject(paymentsFound, 'paymentDate', paymentDate)
                if paymentReturn is not None:
                    self._paymentsAlreadyRead.append(paymentReturn)
                    self._paymentsToSearch.remove(paymentReturn)
                    return paymentReturn

    def returnDayFoundInExtract(self, extract, paymentDate, amountPaid, operation, bank, account, typeComparation):
        # :typeComparation --> 1 = completa (banco e conta corrente); 2 = média (banco); 3 = fraca (apenas valores, data e operação)
        extractDate = extract['dateTransaction']
        extractAmount = extract['amount']
        extractOperation = extract['operation']
        extractBank = extract['bank']
        extractAccount = extract['account']
        search = False

        # caso o valor seja diferente nem processa os dias
        if extractAmount != amountPaid:
            return search

        # caso a diferença entre as datas seja maior que o intervalo definido já retorna falso
        differenceBetweenDates = abs((paymentDate - extractDate).days)
        if differenceBetweenDates > self._numberOfDaysInterval:
            return search

        # procura nos dias positivos e negativos (da data atual até mais 3 dias pra frente/atrás)
        for day in range(0, self._numberOfDaysInterval+1):
            paymentDateComparison = paymentDate + timedelta(days=day)
            paymentDateComparisonLess = paymentDate + timedelta(days=-day)
            if typeComparation == 1:
                if ( extractDate == paymentDateComparison or extractDate == paymentDateComparisonLess ) and extractAmount == amountPaid and extractOperation == operation and extractBank.find(bank) >= 0 and extractAccount.find(account) >= 0:
                    search = True
                    break
            elif typeComparation == 2:
                if ( extractDate == paymentDateComparison or extractDate == paymentDateComparisonLess ) and extractAmount == amountPaid and extractOperation == operation and extractBank.find(bank) >= 0:
                    search = True
                    break
            elif typeComparation == 3:
                if ( extractDate == paymentDateComparison or extractDate == paymentDateComparisonLess ) and extractAmount == amountPaid and extractOperation == operation:
                    search = True
                    break

        return search        

    def returnDataExtract(self, paymentDate, amountPaid, operation, bank='', account=''):
        # o range de 1 a 3 é pq primeiro vou rodar o typeComparation com mais confiabilidade (igual a 1), depois rodo com média e fraca por último
        for numberSequencial in range(1, 4):
            extractsFound = []
            extractReturn = None

            for extract in self._extractsToSearch:
                search = self.returnDayFoundInExtract(extract, paymentDate, amountPaid, operation, bank, account, typeComparation=numberSequencial)
                if search is True:
                    extractsFound.append(extract)
            
            if len(extractsFound) > 0:
                extractReturn = self.findsLessDifferenceBetweenDatesInArrayOfObject(extractsFound, 'dateTransaction', paymentDate)
                if extractReturn is not None:
                    self._extractsExistsInPayments.append(extractReturn)
                    self._extractsToSearch.remove(extractReturn)
                    return extractReturn

    def compareProofWithPayments(self):
        for proof in self._proofOfPayments:
            paymentDate = funcoesUteis.analyzeIfFieldIsValid(proof, 'paymentDate')
            amountPaid = funcoesUteis.analyzeIfFieldIsValid(proof, 'paymentDate')
            bank = funcoesUteis.analyzeIfFieldIsValid(proof, 'bank')
            account = funcoesUteis.analyzeIfFieldIsValid(proof, 'account')

            payment = self.returnDataPayment(paymentDate, amountPaid, bank, account)

            if payment is not None:
                for nameField, valueField in payment.items():
                    if funcoesUteis.analyzeIfFieldIsValid(proof, nameField, None) is None:
                        proof[nameField] = valueField

            # somente o histórico que eu substituo do que está no comprovante de pagamento, mesmo que ele já exista. Pois o histórico do
            # financeiro sempre é melhor do que o está no comprovante
            historicPayment = funcoesUteis.analyzeIfFieldIsValid(payment, 'historic')
            if historicPayment != "":
                proof['historic'] = historicPayment

            self._paymentsFinal.append(proof)

    def comparePaymentsWithProof(self):
        for payment in self._payments:
            existPaymentsInProofOfPayments = list(filter(lambda x: x == payment, self._paymentsAlreadyRead))

            if len(existPaymentsInProofOfPayments) > 0:
                continue
            else:
                payment["foundProof"] = False
                self._paymentsFinal.append(payment)

    # This the end process, he comes the others
    def comparePaymentsFinalWithExtract(self):
        # chama a execução das funções pra não ter que chamá-las duas vezes no main
        self.compareProofWithPayments()
        self.comparePaymentsWithProof()

        extract = []

        for key, paymentFinal in enumerate(self._paymentsFinal):

            operation = funcoesUteis.analyzeIfFieldIsValid(paymentFinal, "operation", "-")
            bank = funcoesUteis.analyzeIfFieldIsValid(paymentFinal, "bank")
            account = funcoesUteis.analyzeIfFieldIsValid(paymentFinal, "account")
            amountPaid = funcoesUteis.analyzeIfFieldIsValid(paymentFinal, "amountPaid", 0.0)
            amountPaidPerLote = funcoesUteis.analyzeIfFieldIsValid(paymentFinal, "amountPaidPerLote", 0.0)
            numberLote = funcoesUteis.analyzeIfFieldIsValid(paymentFinal, "numberLote")
            
            # estas 4 linhas de baixo (principalmente o if) serão utilizadas afim de que quando for o mesmo lote ele retorne a conta do banco pra segunda linha do lote também
            # caso contrário ele retorna só no primeiro, pois depois o valor do extratc é retirado
            previousPaymentFinal = self._paymentsFinal[key-1]
            previousNumberLote = funcoesUteis.analyzeIfFieldIsValid(previousPaymentFinal, "numberLote")
            if previousNumberLote != numberLote or len(self._paymentsFinal) == 1:
                extract = self.returnDataExtract(paymentFinal["paymentDate"], amountPaidPerLote, operation, bank, account)

            # se não conseguir retornar nada ele compara só o amountPaid, talvez no extrato o valor não esteja agrupado, e sim individual
            if extract is None:
                extract = self.returnDataExtract(paymentFinal["paymentDate"], amountPaid, operation, bank, account)
                # se encontrar o valor individual então trocar o numberLote pra um número negativo pra não causar problemas depois na exportação
                if extract is not None:
                    paymentFinal["numberLote"] = (key+1) * -1

            paymentFinal["dateExtract"] = funcoesUteis.analyzeIfFieldIsValid(extract, "dateTransaction")
            paymentFinal["bankExtract"] = f"{funcoesUteis.analyzeIfFieldIsValid(extract, 'bank')}"
            paymentFinal["accountExtract"] = f"{funcoesUteis.analyzeIfFieldIsValid(extract, 'account')}"
            paymentFinal["historicExtract"] = funcoesUteis.analyzeIfFieldIsValid(extract, "historic")            

            # data da importação, importante ela pois nem sempre a data do financeiro do cliente é a certa
            if self._financyIsReliable is True:
                dateOfImport = paymentFinal["paymentDate"]
            else:
                if paymentFinal["dateExtract"] is not None and paymentFinal["dateExtract"] != "":
                    dateOfImport = paymentFinal["dateExtract"]
                else:
                    dateOfImport = paymentFinal["paymentDate"]

            paymentFinal["dateOfImport"] = dateOfImport

            foundProof = funcoesUteis.analyzeIfFieldIsValid(paymentFinal, "foundProof", False)
            if foundProof is True:
                paymentFinal["dateOfImport"] = paymentFinal["paymentDate"]

            self._paymentsFinal[key] = paymentFinal

        return self._paymentsFinal

    # esta função é a responsável por inserir a informação se aquele valor do extrato também existe no pagamento ou não
    def analyseIfExtractIsInPayment(self):
        for extract in self._extracts:
            existProofInPayments = list(filter(lambda x: x == extract, self._extractsExistsInPayments))
            
            if len(existProofInPayments) > 0:
                extract["foundProofInPayments"] = True
            else:
                extract["foundProofInPayments"] = False

            self._extractsFinal.append(extract)
        
        return self._extractsFinal

# if __name__ == "__main__":
    # proofOfPayments = []
    # paymentsCDI = PaymentsCDI()
    # payments = paymentsCDI.processPayments("C:/_temp/integracao_diviart/angio.xlsx")

    # sispagItau = ProofsPaymentsItau()
    # proofOfPayments = sispagItau.process("C:/_temp/integracao_diviart/ARQUIVOCONTAANGIO082019-PAGINA 8.tmp")

    # extractOFX = ExtractsOFX()
    # extracts = extractOFX.process("C:/_temp/integracao_diviart/extratoangio082019.ofx")

    # comparePaymentsAndProofWithExtracts = ComparePaymentsAndProofWithExtracts(extracts, payments, proofOfPayments)
    # print(comparePaymentsAndProofWithExtracts.comparePaymentsFinalWithExtract())