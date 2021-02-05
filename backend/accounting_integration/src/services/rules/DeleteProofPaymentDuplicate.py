import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import tools.funcoesUteis as funcoesUteis
import datetime


class DeleteProofPaymentDuplicate(object):

    def __init__(self, proofPayments=[]):
        self._proofPayments = proofPayments
        self._newExtracts = []
        self._proofPaymentWithOnlyDataNecessary = []
    
    def getDuplicates(self, proofPayment):
        proofsDuplicate = []
        for proofDuplicate in self._proofPaymentWithOnlyDataNecessary:
            if proofDuplicate['paymentDate'] == proofPayment['paymentDate'] and proofDuplicate['nameProvider'] == proofPayment['nameProvider'] and \
                proofDuplicate['cgceProvider'] == proofPayment['cgceProvider'] and proofDuplicate['dueDate'] == proofPayment['dueDate'] and \
                proofDuplicate['bank'] == proofPayment['bank'] and proofDuplicate['account'] == proofPayment['account'] and \
                proofDuplicate['amountPaid'] == proofPayment['amountPaid'] and proofDuplicate['category'] == proofPayment['category']:
                proofsDuplicate.append(proofDuplicate)
        return proofsDuplicate

    def checkIfDuplicate(self, proofPayment) -> bool:
        proofsEquals = self.getDuplicates(proofPayment)
        qtdEqual = 0
        if len(proofsEquals) >= 1:
            for proofEqual in proofsEquals:
                # verifica se em arquivos diferentes tem 2 movimentacao de extrato iguais, caso sim, entao apenas estes irao retornar a informacao de duplicado
                if proofEqual['wayFile'] != proofPayment['wayFile']:
                    qtdEqual += 1
        else:
            qtdEqual = len(proofsEquals)
        return False if qtdEqual < 1 else True

    def process(self):
        for proofPayment in self._proofPayments:
            duplicate = self.checkIfDuplicate(proofPayment)
            if duplicate is not True:
                self._proofPaymentWithOnlyDataNecessary.append(proofPayment)
                self._newExtracts.append(proofPayment)
            else:
                continue

        return self._newExtracts


# if __name__ == '__main__':
#     deleteExtractDuplicate = DeleteExtractDuplicate([{'bank': 'SANTANDER', 'account': '0929130013736', 'typeTransaction': 'OTHER', 'dateTransaction': datetime.date(2020, 10, 1), 'amount': 102.0, 'operation': '-', 'document': '00021811', 'historicCode': 78, 'historic': 'TARIFA MENSALIDADE PACOTE SERVICOS SETEMBRO / 2020', 'wayFile': 'C:/programming/baymax/backend/accounting_integration/data/temp/1418\\ofxs\\extratolvl-2.ofx'}, {'bank': 'SANTANDER', 'account': '0929130013736', 'typeTransaction': 'OTHER', 'dateTransaction': datetime.date(2020, 10, 1), 'amount': 132217.61, 'operation': '+', 'document': '00011001', 'historicCode': 24, 'historic': 'PAGAMENTO A FORNECEDORES MOIP', 'wayFile': 'C:/programming/baymax/backend/accounting_integration/data/temp/1418\\ofxs\\extratolvl-2.ofx'}, {'bank': 'SANTANDER', 'account': '0929130013736', 'typeTransaction': 'OTHER', 'dateTransaction': datetime.date(2020, 10, 1), 'amount': 125772.77, 'operation': '+', 'document': '00011001', 'historicCode': 24, 'historic': 'PAGAMENTO A FORNECEDORES MOIP', 'wayFile': 'C:/programming/baymax/backend/accounting_integration/data/temp/1418\\ofxs\\extratolvl-2.ofx'}, {'bank': 'SANTANDER', 'account': '0929130013736', 'typeTransaction': 'OTHER', 'dateTransaction': datetime.date(2020, 10, 1), 'amount': 1.38, 'operation': '-', 'document': '00111001', 'historicCode': 78, 'historic': 'PGTO FORNECEDORES - TRIB ESTADUAL 0929.4905269217', 'wayFile': 'C:/programmin/baymax/backend/accounting_integration/data/temp/1418\\ofxs\\extratolvl-2.ofx'}, {'bank': 'SANTANDER', 'account': '0929130013736', 'typeTransaction': 'OTHER', 'dateTransaction': datetime.date(2020, 10, 1), 'amount': 1.38, 'operation': '-', 'document': '00111001', 'historicCode': 78, 'historic': 'PGTO FORNECEDORES - TRIB ESTADUAL 0929.4905269217', 'wayFile': 'C:/programming/baymax/backend/accounting_integration/data/temp/1418\\ofxs\\extratolvl-2.ofx'}, {'bank': 'SANTANDER', 'account': '0929130013736', 'typeTransaction': 'OTHER', 'dateTransaction': datetime.date(2020, 10, 1), 'amount': 1.46, 'operation': '-', 'document': '00111001', 'historicCode': 78, 'historic': 'PGTO FORNECEDORES - TRIB ESTADUAL 0929.4905269217', 'wayFile': 'C:/programming/baymax/backend/accounting_integration/data/temp/1418\\ofxs\\extratolvl-2.ofx'}, {'bank': 'SANTANDER', 'account': '0929130013736', 'typeTransaction': 'OTHER', 'dateTransaction': datetime.date(2020, 10, 1), 'amount': 1.49, 'operation': '-', 'document': '00111001', 'historicCode': 78, 'historic': 'PGTO FORNECEDORES - TRIB ESTADUAL 0929.4905269217', 'wayFile': 'C:/programming/baymax/backend/accounting_integration/data/temp/1418\\ofxs\\extratolvl-2.ofx'}, {'bank': 'SANTANDER', 'account': '0929130013736', 'typeTransaction': 'OTHER', 'dateTransaction': datetime.date(2020, 10, 1), 'amount': 1.66, 'operation': '-', 'document': '00111001', 'historicCode': 78, 'historic': 'PGTO FORNECEDORES - TRIB ESTADUAL 0929.4905269217', 'wayFile': 'C:/programming/baymax/backend/accounting_integration/data/temp/1418\\ofxs\\extratolvl-2.ofx'}, {'bank': 'SANTANDER', 'account': '0929130013736', 'typeTransaction': 'OTHER', 'dateTransaction': datetime.date(2020, 10, 1), 'amount': 1.66, 'operation': '-', 'document': '00111001', 'historicCode': 78, 'historic': 'PGTO FORNECEDORES - TRIB ESTADUAL 0929.4905269217', 'wayFile': 'C:/programming/baymax/backend/accounting_integration/data/temp/1418\\ofxs\\extratolvl-2.ofx'}, {'bank': 'SANTANDER', 'account': '0929130013736', 'typeTransaction': 'OTHER', 'dateTransaction': datetime.date(2020, 10, 1), 'amount': 1.66, 'operation': '-', 'document': '00111001', 'historicCode': 78, 'historic': 'PGTO FORNECEDORES - TRIB ESTADUAL 0929.4905269217', 'wayFile': 'C:/programming/baymax/backend/accounting_integration/data/temp/1418\\ofxs\\extratolvl-2.ofx'}, {'bank': 'SANTANDER', 'account': '0929130013736', 'typeTransaction': 'OTHER', 'dateTransaction': datetime.date(2020, 10, 1), 'amount': 1.66, 'operation': '-', 'document': '00111001', 'historicCode': 78, 'historic': 'PGTO FORNECEDORES - TRIB ESTADUAL 0929.4905269217', 'wayFile': 'C:/programming/baymax/backend/accounting_integration/data/temp/1418\\ofxs\\extratolvl-2.ofx'}, {'bank': 'SANTANDER', 'account': '0929130013736', 'typeTransaction': 'OTHER', 'dateTransaction': datetime.date(2020, 10, 1), 'amount': 1.66, 'operation': '-', 'document': '00111001', 'historicCode': 78, 'historic': 'PGTO FORNECEDORES - TRIB ESTADUAL 0929.4905269217', 'wayFile': 'C:/programming/baymax/backend/accounting_integration/data/temp/1418\\ofxs\\extratolvl-2.ofx'}, {'bank': 'SANTANDER', 'account': '0929130013736', 'typeTransaction': 'OTHER', 'dateTransaction': datetime.date(2020, 10, 1), 'amount': 1.66, 'operation': '-', 'document': '00111001', 'historicCode': 78, 'historic': 'PGTO FORNECEDORES - TRIB ESTADUAL 0929.4905269217', 'wayFile': 'C:/programming/baymax/backend/accounting_integration/data/temp/1418\\ofxs\\extratolvl-2.ofx'}])
#     print(deleteExtractDuplicate.process())