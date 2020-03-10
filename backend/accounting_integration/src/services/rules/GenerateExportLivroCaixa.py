import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import json
from datetime import datetime
from operator import itemgetter
import xlsxwriter
import tools.funcoesUteis as funcoesUteis

wayToSaveFiles = open(os.path.join(fileDir, 'backend/accounting_integration/src/WayToSaveFiles.json') )
wayDefault = json.load(wayToSaveFiles)
wayToSaveFiles.close()


class GenerateExportDominio(object):

    def __init__(self, codiEmp, nameFileExport, livroCaixa=[], accountPlan={}):
        self._codiEmp = codiEmp

        self._wayBaseToSaveFiles = os.path.join(wayDefault['WayToSaveFilesOriginals'], f'{self._codiEmp}/arquivos_processados/exportados')
        if os.path.exists(self._wayBaseToSaveFiles) is False:
            os.makedirs(self._wayBaseToSaveFiles)

        self._nameFileExport = f"{funcoesUteis.getOnlyNameFile(nameFileExport)}.txt"
        self._file = open(os.path.join(self._wayBaseToSaveFiles, self._nameFileExport), "w", encoding='utf-8')

        self._livroCaixa = livroCaixa
        self._accountPlan = accountPlan

    def header6000(self):
        idRecord = '6000'
        typeEntry = 'X' # vários débitos pra vários créditos
        codeDefaultEntry = ''
        localizador = ''
        rttFcont = ''

        return f"{idRecord}|{typeEntry}|{codeDefaultEntry}|{localizador}|{rttFcont}|\n"

    def entry6100(self, data):
        idRecord = '6100'
        user = ""
        branch = ""
        scp = ""
        historicCode = 0
        accountCodeDebit = 0
        accountCodeCredit = 0

        dateLivro = funcoesUteis.transformaCampoDataParaFormatoBrasileiro(funcoesUteis.analyzeIfFieldIsValid(data, "dateLivro"))
        movementType = funcoesUteis.analyzeIfFieldIsValid(data, "movementType")
        accountCode = funcoesUteis.analyzeIfFieldIsValid(data, "accountCode")
        historic = funcoesUteis.analyzeIfFieldIsValid(data, "historic")

        amount = funcoesUteis.analyzeIfFieldIsValid(data, "amount")
        amount = str(amount).replace('.', ',')   

        if movementType == "RECEITAS":
            accountCodeDebit = 5
            accountCodeCredit = accountCode
        elif movementType == "DESPESAS":
            accountCodeDebit = accountCode
            accountCodeCredit = 5

        return f"{idRecord}|{dateLivro}|{accountCodeDebit}|{accountCodeCredit}|{amount}|{historicCode}|{historic}|{user}|{branch}|{scp}|\n"

    def entry6140(self, data, key):
        idRecord = '6140'
        natureLaunch = ''
        
        movementType = funcoesUteis.analyzeIfFieldIsValid(data, "movementType")
        document = funcoesUteis.analyzeIfFieldIsValid(data, "document")
        documentType = funcoesUteis.analyzeIfFieldIsValid(data, "documentType")
        participante = funcoesUteis.analyzeIfFieldIsValid(data, "participante", 1)
        imovelRural = funcoesUteis.analyzeIfFieldIsValid(data, "imovelRural", 1)

        if movementType == "RECEITAS":
            movementType = 1
            natureLaunch = 'D'
        elif movementType == "DESPESAS":
            movementType = 2
            natureLaunch = 'C'

        if documentType == "NOTA FISCAL":
            documentType = 1
        elif documentType == "FATURA":
            documentType = 2
        elif documentType == "RECIBO":
            documentType = 3
        elif documentType == "CONTRATO":
            documentType = 4
        elif documentType == "FOLHA DE PAGAMENTO":
            documentType = 5
        elif documentType == "OUTROS":
            documentType = 6

        if movementType > 0 and documentType > 0:
            return f"{idRecord}|{movementType}|{document}|{documentType}|{participante}|{imovelRural}|{natureLaunch}|\n"
        else:
            print(f' \t- ERRO: Na linha {key+2} o "Tipo do Movimento" está errado ou então o "Tipo do Documento".')

    def exportLivroCaixa(self):
        for key, livroCaixa in enumerate(self._livroCaixa):
            account = funcoesUteis.analyzeIfFieldIsValid(livroCaixa, "account")
            accountCode = funcoesUteis.treatNumberField(funcoesUteis.analyzeIfFieldIsValid(self._accountPlan, account), isInt=True)
            livroCaixa['accountCode'] = accountCode

            if accountCode == 0:
                print(f' \t- ERRO: Na linha {key+2} não foi feita a relação da conta {account} com o Plano de Contas')
            
            if accountCode > 0:
                self._file.write(self.header6000())
                self._file.write(self.entry6100(livroCaixa))
                self._file.write(self.entry6140(livroCaixa, key))

    def closeFile(self):
        self._file.close()
