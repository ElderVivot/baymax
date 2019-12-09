import sys
import os

fileDir = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(os.path.join(fileDir, 'backend'))
sys.path.append(os.path.join(fileDir, 'backend/accounting_integration/src/services'))

import json
from datetime import datetime, timedelta
from tools.leArquivos import leXls_Xlsx, leTxt
import tools.funcoesUteis as funcoesUteis
# from read_files.PaymentsCDI import PaymentsCDI
# from read_files.SispagItau import SispagItau
# from read_files.ExtractsOFX import ExtractsOFX


class ComparePaymentsAndProofWithExtracts(object):

    def __init__(self, extracts=[], payments=[], proofOfPayments=[]):
        self._extracts = extracts
        self._payments = payments
        self._proofOfPayments = proofOfPayments
        self._paymentsFinal = []
        self._paymentsAlreadyRead = []
        self._numberOfDaysInterval = { "daysAfter": 3, "daysBefore": 3 }

    def returnDataPayment(self, paymentDate, amountPaid):
        for key, payment in enumerate(self._payments):
            if payment['paymentDate'] == paymentDate and payment['amountPaid'] == amountPaid:
                return [payment, key]

    def returnDayFoundInExtract(self, extract, paymentDate, amountPaid, operation, bank, account):
        paymentDate = funcoesUteis.retornaCampoComoData(paymentDate)
        dayAfter = None
        dayBefore = None

        # procura nos dias positivos (da data atual até mais 3 dias pra frente)
        for day in range(0, self._numberOfDaysInterval["daysAfter"]+1):
            paymentDateComparison = funcoesUteis.transformaCampoDataParaFormatoBrasileiro(paymentDate + timedelta(days=day))
            if extract['dateTransaction'] == paymentDateComparison and extract['amount'] == amountPaid and extract['operation'] == operation \
                    and extract['bankId'] == bank and extract['account'].find(account) > 0:
                dayAfter = day
                break
            if extract['dateTransaction'] == paymentDateComparison and extract['amount'] == amountPaid and extract['operation'] == operation \
                    and extract['bankId'] == bank:
                dayAfter = day
                break
            if extract['dateTransaction'] == paymentDateComparison and extract['amount'] == amountPaid and extract['operation'] == operation:
                dayAfter = day
                break
        
        # se dayAfter é igual a zero quer dizer que o pagamento está no mesmo dia
        if dayAfter == 0:
            return dayAfter

        # procura nos dias negativo (da data atual até menos 3 dias pra trás)
        for day in range(0, self._numberOfDaysInterval["daysBefore"]+1):
            paymentDateComparison = funcoesUteis.transformaCampoDataParaFormatoBrasileiro(paymentDate + timedelta(days=day))
            if extract['dateTransaction'] == paymentDateComparison and extract['amount'] == amountPaid and extract['operation'] == operation \
                    and extract['bankId'] == bank and extract['account'].find(account) > 0:
                dayBefore = day
                break
            if extract['dateTransaction'] == paymentDateComparison and extract['amount'] == amountPaid and extract['operation'] == operation \
                    and extract['bankId'] == bank:
                dayBefore = day
                break
            if extract['dateTransaction'] == paymentDateComparison and extract['amount'] == amountPaid and extract['operation'] == operation:
                dayBefore = day
                break

        # senão encontrar nenhum dia retorna nulto
        if dayAfter is None and dayBefore is None:
            return None
        else:
            if dayAfter < dayBefore:
                return dayAfter
            else:
                dayBefore

    def returnDataExtract(self, paymentDate, amountPaid, operation, bank='', account=''):
        for extract in self._extracts:
            day = self.returnDayFoundInExtract(extract, paymentDate, amountPaid, operation, bank, account)
            if day is not None:
                return extract

    def compareProofWithPayments(self):
        try:
            for proof in self._proofOfPayments:
                paymentArray = self.returnDataPayment(proof["paymentDate"], proof["amountPaid"])
                payment = paymentArray[0]

                proof["document"] = funcoesUteis.analyzeIfFieldIsValid(payment, "document")
                proof["historic"] = funcoesUteis.analyzeIfFieldIsValid(payment, "historic")

                self._paymentsFinal.append(proof)

                self._paymentsAlreadyRead.append(paymentArray[1])
        except Exception as e:
            pass

    def comparePaymentsWithProof(self):
        for key, payment in enumerate(self._payments):
            # se for um pagamento que já leu no comprovante pula ele
            if self._paymentsAlreadyRead.count(key) > 0:
                continue
            else:
                payment["foundProof"] = False
                self._paymentsFinal.append(payment)

    # This the end process, he comes the others
    def comparePaymentsFinalWithExtract(self):
        # chama a execução das funções pra não ter que chamá-las duas vezes no main
        self.compareProofWithPayments()
        self.comparePaymentsWithProof()

        for key, paymentFinal in enumerate(self._paymentsFinal):

            operation = funcoesUteis.analyzeIfFieldIsValid(paymentFinal, "operation", "-")
            bank = funcoesUteis.analyzeIfFieldIsValid(paymentFinal, "bank")
            account = funcoesUteis.analyzeIfFieldIsValid(paymentFinal, "account")

            extract = self.returnDataExtract(paymentFinal["paymentDate"], paymentFinal["amountPaid"], operation, bank, account) 

            paymentFinal["dateExtract"] = funcoesUteis.analyzeIfFieldIsValid(extract, "dateTransaction")
            paymentFinal["bankExtract"] = f"{funcoesUteis.analyzeIfFieldIsValid(extract, 'bankId')}-{funcoesUteis.analyzeIfFieldIsValid(extract, 'account')}"
            paymentFinal["historicExtract"] = funcoesUteis.analyzeIfFieldIsValid(extract, "historic")

            self._paymentsFinal[key] = paymentFinal

        return self._paymentsFinal

# if __name__ == "__main__":
#     paymentsCDI = PaymentsCDI()
#     payments = paymentsCDI.processPayments("C:/_temp/integracao_diviart/angio.xlsx")

#     sispagItau = SispagItau()
#     proofOfPayments = sispagItau.process("C:/_temp/integracao_diviart/ARQUIVOCONTAANGIO082019-PAGINA 8.tmp")

#     extractOFX = ExtractsOFX()
#     extracts = extractOFX.process("C:/_temp/integracao_diviart/extratoangio082019.ofx")

#     comparePaymentsAndProofWithExtracts = ComparePaymentsAndProofWithExtracts(extracts, payments, proofOfPayments)
#     comparePaymentsAndProofWithExtracts.comparePaymentsFinalWithExtract()