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

    def __init__(self, extracts=[], payments=[], proofOfPayments=[]):
        self._extracts = extracts
        self._payments = payments
        self._proofOfPayments = proofOfPayments
        self._paymentsFinal = []
        self._paymentsAlreadyRead = []
        self._extractsExistsInPayments = [] # este daqui são para os extratos que encontrou correlação nos pagamentos, na planilha de extratos conterá um campo com esta informação
        self._extractsFinal = []
        self._numberOfDaysInterval = { "daysAfter": 3, "daysBefore": 3 }

    def returnDayFoundInPayment(self, payment, paymentDate, amountPaid):
        paymentDate = funcoesUteis.retornaCampoComoData(paymentDate)
        dayAfter = None
        dayBefore = None

        # olha até 10 dias a mais
        for day in range(0, 11):
            paymentDateComparison = funcoesUteis.transformaCampoDataParaFormatoBrasileiro(paymentDate + timedelta(days=day))
            if payment['paymentDate'] == paymentDateComparison and payment['amountPaid'] == amountPaid:
                dayAfter = day
                break
        
        # se dayAfter é igual a zero quer dizer que o pagamento está no mesmo dia
        if dayAfter == 0:
            return dayAfter

        # olha até 10 dias a menos
        for day in range(1, 11):
            paymentDateComparison = funcoesUteis.transformaCampoDataParaFormatoBrasileiro(paymentDate + timedelta(days=-day))
            if payment['paymentDate'] == paymentDateComparison and payment['amountPaid'] == amountPaid:
                dayBefore = day
                break

        # senão encontrar nenhum dia retorna nulo
        if dayAfter is None and dayBefore is None:
            return None
        else:
            if dayAfter is None and dayBefore is not None:
                return dayBefore
            if dayAfter is not None and dayBefore is None:
                return dayAfter
                
            if dayAfter < dayBefore:
                return dayAfter
            else:
                return dayBefore

    def returnDataPayment(self, paymentDate, amountPaid):
        for key, payment in enumerate(self._payments):
            day = self.returnDayFoundInPayment(payment, paymentDate, amountPaid)
            if day is not None:
                return [payment, key] # o key eu retorno pra depois identificar quais pagamentos já foram processados nas provas de pagamentos e não imprimi-los novamente

    def returnDayFoundInExtract(self, extract, paymentDate, amountPaid, operation, bank, account):
        paymentDate = funcoesUteis.retornaCampoComoData(paymentDate)
        dayAfter = None
        dayBefore = None

        # procura nos dias positivos (da data atual até mais 3 dias pra frente)
        for day in range(0, self._numberOfDaysInterval["daysAfter"]+1):
            paymentDateComparison = funcoesUteis.transformaCampoDataParaFormatoBrasileiro(paymentDate + timedelta(days=day))
            print(extract['amount'], extract['dateTransaction'], paymentDateComparison, day)
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
        for day in range(1, self._numberOfDaysInterval["daysBefore"]+1):
            paymentDateComparison = funcoesUteis.transformaCampoDataParaFormatoBrasileiro(paymentDate + timedelta(days=-day)) # - (menos) day pois estou voltando data
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

        # senão encontrar nenhum dia retorna nulo
        if dayAfter is None and dayBefore is None:
            return None
        else:
            if dayAfter is None and dayBefore is not None:
                return dayBefore
            if dayAfter is not None and dayBefore is None:
                return dayAfter
                
            if dayAfter < dayBefore:
                return dayAfter
            else:
                return dayBefore

    def returnDataExtract(self, paymentDate, amountPaid, operation, bank='', account=''):
        for extract in self._extracts:
            day = self.returnDayFoundInExtract(extract, paymentDate, amountPaid, operation, bank, account)
            if day is not None:
                return extract

    def compareProofWithPayments(self):
        for proof in self._proofOfPayments:
            paymentArray = self.returnDataPayment(proof["paymentDate"], proof["amountPaid"])
            try:
                payment = paymentArray[0]

                self._paymentsAlreadyRead.append(paymentArray[1])
            except Exception:
                payment = []
            
            proof["foundProof"] = True
            proof["document"] = funcoesUteis.analyzeIfFieldIsValid(payment, "document")
            proof["historic"] = funcoesUteis.analyzeIfFieldIsValid(payment, "historic")
            proof["amountDiscount"] = funcoesUteis.analyzeIfFieldIsValid(payment, "amountDiscount")
            proof["amountInterest"] = funcoesUteis.analyzeIfFieldIsValid(payment, "amountInterest")
            proof["amountOriginal"] = funcoesUteis.analyzeIfFieldIsValid(payment, "amountOriginal")
            proof["accountPlan"] = funcoesUteis.analyzeIfFieldIsValid(payment, "accountPlan")
            proof["bankCheck"] = funcoesUteis.analyzeIfFieldIsValid(payment, "bankCheck")

            self._paymentsFinal.append(proof)

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
            if extract is not None:
                self._extractsExistsInPayments.append(extract)

            paymentFinal["dateExtract"] = funcoesUteis.analyzeIfFieldIsValid(extract, "dateTransaction")
            paymentFinal["bankExtract"] = f"{funcoesUteis.analyzeIfFieldIsValid(extract, 'bankId')}"
            paymentFinal["accountExtract"] = f"{funcoesUteis.analyzeIfFieldIsValid(extract, 'account')}"
            paymentFinal["historicExtract"] = funcoesUteis.analyzeIfFieldIsValid(extract, "historic")

            # data da importação, importante ela pois nem sempre a data do financeiro do cliente é a certa
            if extract is None:
                dateOfImport = paymentFinal["paymentDate"]
            else:
                dateOfImport = paymentFinal["dateExtract"]
            
            paymentFinal["dateOfImport"] = dateOfImport

            foundProof = funcoesUteis.analyzeIfFieldIsValid(paymentFinal, "foundProof", False)
            if foundProof is True:
                paymentFinal["dateOfImport"] = paymentFinal["paymentDate"]

            self._paymentsFinal[key] = paymentFinal

        return self._paymentsFinal

    def analyseIfExtractIsInPayment(self):
        for extract in self._extracts:
            existProofInPayments = list(filter(lambda x: x == extract, self._extractsExistsInPayments))
            
            if len(existProofInPayments) > 0:
                extract["foundProofInPayments"] = True
            else:
                extract["foundProofInPayments"] = False

            self._extractsFinal.append(extract)
        
        return self._extractsFinal

if __name__ == "__main__":
    payments = [{'paymentDate': '01/10/2019', 'nameProvider': 'BANCO DO BRASIL', 'cgceProvider': '00000000000191', 'document': '1102019', 'parcelNumber': '', 'bank': 'BB', 'account': '69000',     'amountPaid': 1.39, 'amountDiscount': 0.0, 'amountInterest': 0.0, 'amountOriginal': 0.0, 'amountFine': 0.0, 'amountDevolution': 0.0, 'paymentType': '', 'accountPlan': 'TARIFAS DE COBRANCA', 'historic': '', 'companyBranch': ''}, {'paymentDate': '01/10/2019', 'nameProvider': 'BANCO DO BRASIL', 'cgceProvider': '00000000000191', 'document': '1102019', 'parcelNumber': '', 'bank': 'BB', 'account': '69000',     'amountPaid': 1.39, 'amountDiscount': 0.0, 'amountInterest': 0.0, 'amountOriginal': 0.0, 'amountFine': 0.0, 'amountDevolution': 0.0, 'paymentType': '', 'accountPlan': 'TARIFAS DE COBRANCA', 'historic': '', 'companyBranch': ''}, {'paymentDate': '01/10/2019', 'nameProvider': 'BANCO DO BRASIL', 'cgceProvider': '00000000000191', 'document': '1102019', 'parcelNumber': '', 'bank': 'BB', 'account': '69000',     'amountPaid': 15.0, 'amountDiscount': 0.0, 'amountInterest': 0.0, 'amountOriginal': 0.0, 'amountFine': 0.0, 'amountDevolution': 0.0, 'paymentType': '', 'accountPlan': 'TARIFAS BANCARIAS / MANUTENCAO DE CONTA', 'historic': '', 'companyBranch': ''}, {'paymentDate': '01/10/2019', 'nameProvider': 'BANCO DO BRASIL', 'cgceProvider': '00000000000191', 'document': '1102019', 'parcelNumber': '', 'bank': 'BB', 'account': '69000',     'amountPaid': 11390.03, 'amountDiscount': 0.0, 'amountInterest': 0.0, 'amountOriginal': 0.0, 'amountFine': 0.0, 'amountDevolution': 0.0, 'paymentType': '', 'accountPlan': 'APLICACAO AUT', 'historic': '', 'companyBranch': ''}, {'paymentDate': '02/10/2019', 'nameProvider': 'BANCO DO BRASIL', 'cgceProvider': '00000000000191', 'document': '2102019', 'parcelNumber': '', 'bank': 'BB', 'account': '69000',     'amountPaid': 1.39, 'amountDiscount': 0.0, 'amountInterest': 0.0, 'amountOriginal': 0.0, 'amountFine': 0.0, 'amountDevolution': 0.0, 'paymentType': '', 'accountPlan': 'TARIFAS DE COBRANCA', 'historic': '', 'companyBranch': ''}, {'paymentDate': '02/10/2019', 'nameProvider': 'BANCO DO BRASIL', 'cgceProvider': '00000000000191', 'document': '2102019', 'parcelNumber': '', 'bank': 'BB', 'account': '69000',     'amountPaid': 2.78, 'amountDiscount': 0.0, 'amountInterest': 0.0, 'amountOriginal': 0.0, 'amountFine': 0.0, 'amountDevolution': 0.0, 'paymentType': '', 'accountPlan': 'TARIFAS DE COBRANCA', 'historic': '', 'companyBranch': ''}]
    extracts = [{'bankId': 'BRASIL', 'account': '69000-7', 'typeTransaction': 'DEP', 'dateTransaction': '01/10/2019', 'amount': 11407.81, 'operation': '+', 'document': '00004146', 'historicCode': 24, 'historic': 'COBRANCA'}, {'bankId': 'BRASIL', 'account': '69000-7', 'typeTransaction': 'DEBIT', 'dateTransaction': '01/10/2019', 'amount': 1.39, 'operation': '-', 'document': '00004941', 'historicCode': 78, 'historic': 'DEBITO SERVICO COBRANCA'}, {'bankId': 'BRASIL', 'account': '69000-7', 'typeTransaction': 'DEBIT', 'dateTransaction': '01/10/2019', 'amount': 1.39, 'operation': '-', 'document': '00043083', 'historicCode': 78, 'historic': 'DEBITO SERVICO COBRANCA'}, {'bankId': 'BRASIL', 'account': '69000-7', 'typeTransaction': 'DEBIT', 'dateTransaction': '01/10/2019', 'amount': 15.0, 'operation': '-', 'document': '00153797', 'historicCode': 78, 'historic': 'TARIFA CHEQUE OURO MANUT'}, {'bankId': 'BRASIL', 'account': '69000-7', 'typeTransaction': 'DEBIT', 'dateTransaction': '01/10/2019', 'amount': 11390.03, 'operation': '-', 'document': '5', 'historicCode': 78, 'historic': 'BB CP AUTOMATICO EMPRESA'}, {'bankId': 'BRASIL', 'account': '69000-7', 'typeTransaction': 'DEP', 'dateTransaction': '02/10/2019', 'amount': 5650.69, 'operation': '+', 'document': '00009808', 'historicCode': 24, 'historic': 'COBRANCA'}, {'bankId': 'BRASIL', 'account': '69000-7', 'typeTransaction': 'DEBIT', 'dateTransaction': '02/10/2019', 'amount': 65000.0, 'operation': '-', 'document': '100201', 'historicCode': 78, 'historic': 'TED'}, {'bankId': 'BRASIL', 'account': '69000-7', 'typeTransaction': 'DEBIT', 'dateTransaction': '02/10/2019', 'amount': 1.39, 'operation': '-', 'document': '00004680', 'historicCode': 78, 'historic': 'DEBITO SERVICO COBRANCA'}, {'bankId': 'BRASIL', 'account': '69000-7', 'typeTransaction': 'DEBIT', 'dateTransaction': '02/10/2019', 'amount': 2.78, 'operation': '-', 'document': '00040320', 'historicCode': 78, 'historic': 'DEBITO SERVICO COBRANCA'}, {'bankId': 'BRASIL', 'account': '69000-7', 'typeTransaction': 'DEP', 'dateTransaction': '02/10/2019', 'amount': 55823.46, 'operation': '+', 'document': '5', 'historicCode': 24, 'historic': 'BB CP AUTOMATICO EMPRESA'}, {'bankId': 'BRASIL', 'account': '69000-7', 'typeTransaction': 'DEP', 'dateTransaction': '02/10/2019', 'amount': 3530.02, 'operation': '+', 'document': '1100', 'historicCode': 24, 'historic': 'FUNDO BB RF SIMPLES'}]
    proofOfPayments = []
    # paymentsCDI = PaymentsCDI()
    # payments = paymentsCDI.processPayments("C:/_temp/integracao_diviart/angio.xlsx")

    # sispagItau = ProofsPaymentsItau()
    # proofOfPayments = sispagItau.process("C:/_temp/integracao_diviart/ARQUIVOCONTAANGIO082019-PAGINA 8.tmp")

    # extractOFX = ExtractsOFX()
    # extracts = extractOFX.process("C:/_temp/integracao_diviart/extratoangio082019.ofx")

    comparePaymentsAndProofWithExtracts = ComparePaymentsAndProofWithExtracts(extracts, payments, proofOfPayments)
    print(comparePaymentsAndProofWithExtracts.comparePaymentsFinalWithExtract())