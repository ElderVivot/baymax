import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

from tools.leArquivos import leXls_Xlsx, leTxt, readJson
import tools.funcoesUteis as funcoesUteis


class LivroCaixaRural(object):

    def __init__(self, codiEmp, wayOriginalToRead):
        self._codiEmp = codiEmp
        self._wayOriginalToRead = wayOriginalToRead
        self._livroCaixaRural = []
        self._accountPlan = {}

    def processAccountPlan(self, dataFile):
        for key, data in enumerate(dataFile):

            try:
                recordType = data[0:2]
                account = data[2:10]
                nameAccount = funcoesUteis.treatTextField(data[246:356])
                nameAccountMain = funcoesUteis.treatTextField(data[26:136])
                nameAccountSubMain = funcoesUteis.treatTextField(data[136:246])

                if recordType == '05':
                    self._accountPlan[account] = [nameAccount, nameAccountMain, nameAccountSubMain]

            except Exception as e:
                pass

    def searchIfANote(self, historic):
        positionNote = -1
        noteCorrect = ""

        if historic.find(' NUMERO') >= 0:
            positionNote = historic.find(' NUMERO') + len(' NUMERO')

        if historic.find(' CUPOM') >= 0:
            positionNote = historic.find(' CUPOM') + len(' NUMERO')

        if historic.find(' NF') >= 0:
            positionNote = historic.find(' NF') + len(' NF')

        if positionNote >= 0:
            note = historic[positionNote:].lstrip()
            noteSplitHyphen = note.split('-')
            noteSplitSpace = note.split(' ')

            noteHyphenOne = funcoesUteis.analyzeIfFieldIsValidMatrix(noteSplitHyphen, 1).strip()
            noteHyphenTwo = funcoesUteis.analyzeIfFieldIsValidMatrix(noteSplitHyphen, 2).strip()
            if noteHyphenOne == "":
                noteHyphen = noteHyphenTwo.split(' ')[0].strip()
            else:
                noteHyphen = noteHyphenOne

            noteSpace = funcoesUteis.analyzeIfFieldIsValidMatrix(noteSplitSpace, 1).strip()
            if noteSpace.find('-') >= 0:
                noteCorrect = noteHyphen
            else:
                noteCorrect = noteSpace

            noteIsNumeric = funcoesUteis.treatNumberField(noteCorrect, isInt=True)
            if noteIsNumeric > 0:
                noteCorrect == noteCorrect
            else:
                noteCorrect = ""
        
        return noteCorrect

    def process(self, file):
        dataFile = leTxt(file)

        self.processAccountPlan(dataFile)

        valuesOfLine = {}
        valuesOfFile = []

        for key, data in enumerate(dataFile):

            try:
                recordType = data[0:2]
                dateLivro = funcoesUteis.retornaCampoComoData(data[3:11], 4)
                account = data[11:19]
                nameAccount = funcoesUteis.analyzeIfFieldIsValid(self._accountPlan, account)[0]
                historic = funcoesUteis.treatTextField(data[19:274])
                amount = funcoesUteis.treatDecimalField(f'{data[274:285]},{data[285:287]}')

                note = self.searchIfANote(historic)
                if note != "":
                    documentType = 1
                else:
                    documentType = 2

                if account[0] == "1":
                    movementType = 'Receitas'
                else:
                    movementType = 'Despesas'

                if recordType == "03":
                    valuesOfLine = {
                        'dateLivro': dateLivro,
                        'movementType':movementType,
                        'account': account,
                        'nameAccount': nameAccount,
                        'amount': amount,
                        'document': note,
                        'documentType': documentType,
                        'historic': historic
                    }            

                valuesOfFile.append(valuesOfLine.copy())

            except Exception as e:
                pass

        return valuesOfFile

    def processAll(self):
        for root, dirs, files in os.walk(self._wayOriginalToRead):
            for file in files:
                wayFile = os.path.join(root, file)

                if file.lower().endswith(('.dbk', '.txt')):
                    self._livroCaixaRural.append(self.process(wayFile))

        return [ funcoesUteis.removeAnArrayFromWithinAnother(self._livroCaixaRural), self._accountPlan ]


if __name__ == "__main__":

    livroCaixaRural = LivroCaixaRural(1593, 'C:/integracao_contabil/1593/arquivos_originais')
    print(livroCaixaRural.processAll())

