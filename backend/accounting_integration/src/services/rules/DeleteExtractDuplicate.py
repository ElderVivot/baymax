import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import tools.funcoesUteis as funcoesUteis
import datetime


class DeleteExtractDuplicate(object):

    def __init__(self, extracts=[]):
        self._extracts = extracts
        self._newExtracts = []
        self._extractsWithOnlyDataNecessary = []

    def cleanExtractWithOnlyDataNecessary(self, extract):
        del extract['historicCode']
        del extract['historic']
        document = funcoesUteis.analyzeIfFieldIsValid(extract, "document", None)
        document = funcoesUteis.treatNumberField(document, isInt=True)
        extract['document'] = document
        return extract

    def getDuplicates(self, extract):
        extractsDuplicate = []
        for extractDuplicate in self._extractsWithOnlyDataNecessary:
            if extractDuplicate['bank'] == extract['bank'] and extractDuplicate['account'] == extract['account'] and \
                extractDuplicate['typeTransaction'] == extract['typeTransaction'] and extractDuplicate['dateTransaction'] == extract['dateTransaction'] and \
                extractDuplicate['amount'] == extract['amount'] and extractDuplicate['operation'] == extract['operation'] and \
                extractDuplicate['document'] == extract['document']:
                extractsDuplicate.append(extractDuplicate)
        return extractsDuplicate

    def checkIfDuplicate(self, extract) -> bool:
        extractsEquals = self.getDuplicates(extract)
        qtdEqual = 0
        if len(extractsEquals) >= 1:
            for extractEqual in extractsEquals:
                # verifica se em arquivos diferentes tem 2 movimentacao de extrato iguais, caso sim, entao apenas estes irao retornar a informacao de duplicado
                if extractEqual['wayFile'] != extract['wayFile']:
                    qtdEqual += 1
        else:
            qtdEqual = len(extractsEquals)
        return False if qtdEqual < 1 else True

    def process(self):
        for extract in self._extracts:
            # newExtract = self.cleanExtractWithOnlyDataNecessary(extract.copy())
            duplicateExtract = self.checkIfDuplicate(extract)
            if duplicateExtract is not True:
                self._extractsWithOnlyDataNecessary.append(extract)
                self._newExtracts.append(extract)
            else:
                continue

        return self._newExtracts


if __name__ == '__main__':
    deleteExtractDuplicate = DeleteExtractDuplicate([{'bank': 'SANTANDER', 'account': '0929130013736', 'typeTransaction': 'OTHER', 'dateTransaction': datetime.date(2020, 10, 1), 'amount': 102.0, 'operation': '-', 'document': '00021811', 'historicCode': 78, 'historic': 'TARIFA MENSALIDADE PACOTE SERVICOS SETEMBRO / 2020', 'wayFile': 'C:/programming/baymax/backend/accounting_integration/data/temp/1418\\ofxs\\extratolvl-2.ofx'}, {'bank': 'SANTANDER', 'account': '0929130013736', 'typeTransaction': 'OTHER', 'dateTransaction': datetime.date(2020, 10, 1), 'amount': 132217.61, 'operation': '+', 'document': '00011001', 'historicCode': 24, 'historic': 'PAGAMENTO A FORNECEDORES MOIP', 'wayFile': 'C:/programming/baymax/backend/accounting_integration/data/temp/1418\\ofxs\\extratolvl-2.ofx'}, {'bank': 'SANTANDER', 'account': '0929130013736', 'typeTransaction': 'OTHER', 'dateTransaction': datetime.date(2020, 10, 1), 'amount': 125772.77, 'operation': '+', 'document': '00011001', 'historicCode': 24, 'historic': 'PAGAMENTO A FORNECEDORES MOIP', 'wayFile': 'C:/programming/baymax/backend/accounting_integration/data/temp/1418\\ofxs\\extratolvl-2.ofx'}, {'bank': 'SANTANDER', 'account': '0929130013736', 'typeTransaction': 'OTHER', 'dateTransaction': datetime.date(2020, 10, 1), 'amount': 1.38, 'operation': '-', 'document': '00111001', 'historicCode': 78, 'historic': 'PGTO FORNECEDORES - TRIB ESTADUAL 0929.4905269217', 'wayFile': 'C:/programmin/baymax/backend/accounting_integration/data/temp/1418\\ofxs\\extratolvl-2.ofx'}, {'bank': 'SANTANDER', 'account': '0929130013736', 'typeTransaction': 'OTHER', 'dateTransaction': datetime.date(2020, 10, 1), 'amount': 1.38, 'operation': '-', 'document': '00111001', 'historicCode': 78, 'historic': 'PGTO FORNECEDORES - TRIB ESTADUAL 0929.4905269217', 'wayFile': 'C:/programming/baymax/backend/accounting_integration/data/temp/1418\\ofxs\\extratolvl-2.ofx'}, {'bank': 'SANTANDER', 'account': '0929130013736', 'typeTransaction': 'OTHER', 'dateTransaction': datetime.date(2020, 10, 1), 'amount': 1.46, 'operation': '-', 'document': '00111001', 'historicCode': 78, 'historic': 'PGTO FORNECEDORES - TRIB ESTADUAL 0929.4905269217', 'wayFile': 'C:/programming/baymax/backend/accounting_integration/data/temp/1418\\ofxs\\extratolvl-2.ofx'}, {'bank': 'SANTANDER', 'account': '0929130013736', 'typeTransaction': 'OTHER', 'dateTransaction': datetime.date(2020, 10, 1), 'amount': 1.49, 'operation': '-', 'document': '00111001', 'historicCode': 78, 'historic': 'PGTO FORNECEDORES - TRIB ESTADUAL 0929.4905269217', 'wayFile': 'C:/programming/baymax/backend/accounting_integration/data/temp/1418\\ofxs\\extratolvl-2.ofx'}, {'bank': 'SANTANDER', 'account': '0929130013736', 'typeTransaction': 'OTHER', 'dateTransaction': datetime.date(2020, 10, 1), 'amount': 1.66, 'operation': '-', 'document': '00111001', 'historicCode': 78, 'historic': 'PGTO FORNECEDORES - TRIB ESTADUAL 0929.4905269217', 'wayFile': 'C:/programming/baymax/backend/accounting_integration/data/temp/1418\\ofxs\\extratolvl-2.ofx'}, {'bank': 'SANTANDER', 'account': '0929130013736', 'typeTransaction': 'OTHER', 'dateTransaction': datetime.date(2020, 10, 1), 'amount': 1.66, 'operation': '-', 'document': '00111001', 'historicCode': 78, 'historic': 'PGTO FORNECEDORES - TRIB ESTADUAL 0929.4905269217', 'wayFile': 'C:/programming/baymax/backend/accounting_integration/data/temp/1418\\ofxs\\extratolvl-2.ofx'}, {'bank': 'SANTANDER', 'account': '0929130013736', 'typeTransaction': 'OTHER', 'dateTransaction': datetime.date(2020, 10, 1), 'amount': 1.66, 'operation': '-', 'document': '00111001', 'historicCode': 78, 'historic': 'PGTO FORNECEDORES - TRIB ESTADUAL 0929.4905269217', 'wayFile': 'C:/programming/baymax/backend/accounting_integration/data/temp/1418\\ofxs\\extratolvl-2.ofx'}, {'bank': 'SANTANDER', 'account': '0929130013736', 'typeTransaction': 'OTHER', 'dateTransaction': datetime.date(2020, 10, 1), 'amount': 1.66, 'operation': '-', 'document': '00111001', 'historicCode': 78, 'historic': 'PGTO FORNECEDORES - TRIB ESTADUAL 0929.4905269217', 'wayFile': 'C:/programming/baymax/backend/accounting_integration/data/temp/1418\\ofxs\\extratolvl-2.ofx'}, {'bank': 'SANTANDER', 'account': '0929130013736', 'typeTransaction': 'OTHER', 'dateTransaction': datetime.date(2020, 10, 1), 'amount': 1.66, 'operation': '-', 'document': '00111001', 'historicCode': 78, 'historic': 'PGTO FORNECEDORES - TRIB ESTADUAL 0929.4905269217', 'wayFile': 'C:/programming/baymax/backend/accounting_integration/data/temp/1418\\ofxs\\extratolvl-2.ofx'}, {'bank': 'SANTANDER', 'account': '0929130013736', 'typeTransaction': 'OTHER', 'dateTransaction': datetime.date(2020, 10, 1), 'amount': 1.66, 'operation': '-', 'document': '00111001', 'historicCode': 78, 'historic': 'PGTO FORNECEDORES - TRIB ESTADUAL 0929.4905269217', 'wayFile': 'C:/programming/baymax/backend/accounting_integration/data/temp/1418\\ofxs\\extratolvl-2.ofx'}])
    print(deleteExtractDuplicate.process())