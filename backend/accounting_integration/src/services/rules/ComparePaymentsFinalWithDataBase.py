# coding: utf-8

import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))
sys.path.append(os.path.join(fileDir, 'backend/accounting_integration/src/services'))

import json
from math import floor
from datetime import datetime, timedelta
from tools.leArquivos import leXls_Xlsx, leTxt, readJson
import tools.funcoesUteis as funcoesUteis


class ComparePaymentsFinalWithDataBase(object):
    
    def __init__(self, codiEmp, finalDate, providers=[], entryNotes=[], installments=[], payments=[]):
        self._providers = providers
        self._entryNotes = entryNotes
        self._payments = payments
        self._installments = installments
        self._codiEmp = codiEmp
        self._finalDate = funcoesUteis.retornaCampoComoData(finalDate)
        self._paymentsFinal = []
        self._listWordsNotConsiderInTheName = ['LTDA', 'LTDA.', '-', 'ME', 'ME.', 'EPP', 'EPP.', 'EIRELI', 'EIRELI.', \
            'MEI', 'MEI.', 'EI', 'EI.', 'S.A.', 'SA', 'S.A', 'S/A']
        self._listWordsAbbreviatedToChange = {
            "COM.": "COMERCIO",
            "PROD.": "PRODUCAO",
            "IND.": "INDUSTRIA",
            "IMP.": "IMPORTACAO",
            "EXP.": "EXPORTACAO",
            "MAT.": "MATERIAIS",
            "LIMP.": "LIMPEZA",
            "SERV.": "SERVICO",
            "EQUIP.": "EQUIPAMENTOS",
            "P/": "PARA",
            "ARTIG.": "ARTIGOS",
            "DIST.": "DISTRIBUIDORA",
            "CONST.": "CONSTRUCAO"
        }

    def changeAbbreviatedWord(self, name):
        try:
            nameChanged = ""
            for wordName in name.split():
                def chechWordIsInTheList():
                    for abbreviate, wordToChange in self._listWordsAbbreviatedToChange.items():
                        if wordName == abbreviate:
                            return wordToChange
                
                wordNew = chechWordIsInTheList()
                if wordNew is not None:
                    nameChanged = f"{nameChanged} {wordNew}"
                else:
                    nameChanged = f"{nameChanged} {wordName}"
            nameChanged = funcoesUteis.minimalizeSpaces(nameChanged)

            return nameChanged
        except Exception:
            return ""
    
    def removeWordsThatAreNotNames(self, name):
        try:
            nameChanged = ""
            for wordName in name.split():
                def chechWordIsInTheList():
                    for listWordNotConsider in self._listWordsNotConsiderInTheName:
                        if wordName == listWordNotConsider:
                            return True
                
                # adiciona apenas as palavras que não estão na lista
                if chechWordIsInTheList() is None:
                    nameChanged = f"{nameChanged} {wordName}"
            nameChanged = funcoesUteis.minimalizeSpaces(nameChanged)

            return nameChanged
        except Exception:
            return ""

    def compareTwoNames(self, nameOne, nameTwo):
        nameOne = self.changeAbbreviatedWord(self.removeWordsThatAreNotNames(nameOne))
        nameTwo = self.changeAbbreviatedWord(self.removeWordsThatAreNotNames(nameTwo))

        nameOneSplit = nameOne.split(' ')

        countEqualWords = 0

        nameTwoSplit = nameTwo.split(' ')
        for wordName in nameTwoSplit:
            if nameOneSplit.count(wordName) > 0: # conta somente as palavras em comuns
                countEqualWords += 1

        percentWordsEqualsAboutNameOne = countEqualWords / len(nameOneSplit)
        percentWordsEqualsAboutNameTwo = countEqualWords / len(nameTwoSplit)
        
        if nameOne[:7] == nameTwo[:7]:
            first7LettersEquals = True
        else:
            first7LettersEquals = False

        if nameOne[:12] == nameTwo[:12]:
            first12LettersEquals = True
        else:
            first12LettersEquals = False

        if nameOne[:20] == nameTwo[:20]:
            first20LettersEquals = True
        else:
            first20LettersEquals = False

        return {
            "countLettersNameOne": len(nameOne),
            "countWordsNameOne": len(nameOneSplit),
            "countLettersNameTwo": len(nameTwo),
            "countWordsNameTwo": len(nameTwoSplit),
            "countEqualWords": countEqualWords,
            "first7LettersEquals": first7LettersEquals,
            "first12LettersEquals": first12LettersEquals,
            "first20LettersEquals": first20LettersEquals,
            "percentWordsEqualsAboutNameOne": percentWordsEqualsAboutNameOne,
            "percentWordsEqualsAboutNameTwo": percentWordsEqualsAboutNameTwo
        }

    def returnDataProvider(self, codi_for=0, cgce=None, name=None, degreeOfReliability=0):
        # caso os campos sejam vazios deixa eles como nulos
        if cgce == "":
            cgce = None
        if name == "":
            name = None

        for provider in self._providers:

            provider['cgce_for_original'] = provider['cgce_for']
            provider['cgce_for'] = "" if provider['cgce_for'] is None else provider['cgce_for'][:12]

            if int(provider['codi_for']) == int(codi_for):
                return provider

            # pega só os 12 primeiros caracteres pois os dois últimos são apenas de validação do cnpj. Já se for CPF pega todos normal
            if provider['cgce_for_original'] == cgce and cgce is not None:
                return provider

            # agora as verificações pelo nome (esta primeira tem grau alto de confiabilidade)
            if name is None:
                continue

            nameProvider = self.changeAbbreviatedWord(self.removeWordsThatAreNotNames(provider["nome_for"]))
            nameArgument = self.changeAbbreviatedWord(self.removeWordsThatAreNotNames(name))

            def findProviderForName():
                compareTwoNames = self.compareTwoNames(nameProvider, nameArgument)
                if compareTwoNames['percentWordsEqualsAboutNameOne'] > 0.75 and compareTwoNames['percentWordsEqualsAboutNameTwo'] > 0.75:
                    return provider

            if findProviderForName() is not None:
                return provider

    def returnDataEntryNote(self, note=0, cgceProvider=None, ddoc_ent = None, dent_ent = None, amountPayment = 0.0, nameProvider=None, dueDate=None, amountOriginal=0.0):
        if note == "" or note is None:
            note = 0
        if cgceProvider == "":
            cgceProvider = None
        if ddoc_ent == "":
            ddoc_ent = None
        if dent_ent == "":
            dent_ent = None
        if dueDate == "":
            dueDate = None
        if nameProvider == "":
            nameProvider = None

        note = funcoesUteis.treatNumberField(note, True)

        if note == 0 and ddoc_ent is None and dent_ent is None and cgceProvider is None and nameProvider is None:
            return None

        wayFiles = os.path.join(fileDir, 'backend/extract/data/entradas/', str(self._codiEmp))

        for root, dirs, files in os.walk(wayFiles):
            for file in sorted(files, reverse=True):
                if file.lower().endswith(('.json')):
                    competenceFile = funcoesUteis.retornaCampoComoData(f'{file[0:4]}-{file[4:6]}-01', 2)
                    if competenceFile > self._finalDate:
                        continue

                    wayFile = os.path.join(root, file)
                    entryNotes = readJson(wayFile)

                    for entryNote in entryNotes:
                        provider = self.returnDataProvider(entryNote["codi_for"])

                        cgceProviderEntryNote = funcoesUteis.analyzeIfFieldIsValid(provider, "cgce_for", None)
                        nameProviderEntryNote = funcoesUteis.analyzeIfFieldIsValid(provider, "nome_for", None)
                        noteEntryNote = int(funcoesUteis.analyzeIfFieldIsValid(entryNote, "nume_ent", 0))
                        issueEntryNote = funcoesUteis.transformaCampoDataParaFormatoBrasileiro( \
                            funcoesUteis.retornaCampoComoData(funcoesUteis.analyzeIfFieldIsValid(entryNote, "ddoc_ent"), 2) )
                        entryEntryNote = funcoesUteis.transformaCampoDataParaFormatoBrasileiro( \
                            funcoesUteis.retornaCampoComoData(funcoesUteis.analyzeIfFieldIsValid(entryNote, "dent_ent"), 2) )
                        amountAccountEntryNote = float(funcoesUteis.analyzeIfFieldIsValid(entryNote, "vcon_ent", 0.0))

                        if note != 0: # se a nota for válida compara os dados com ela, uma comparação no mínimo tem que ser igual, pq a se a nota tá preenchida ela tem que existir na domínio (mesmo número)
                            if noteEntryNote == note and cgceProviderEntryNote == cgceProvider:
                                return entryNote

                            if noteEntryNote == note and issueEntryNote == ddoc_ent and ddoc_ent is not None:
                                return entryNote

                            if noteEntryNote == note and entryEntryNote == dent_ent and dent_ent is not None:
                                return entryNote

                            if noteEntryNote == note and issueEntryNote == dueDate and dueDate is not None: # a comparação por vencimento e emissão é pq algumas vezes a data de vencimento é a própria emissão
                                return entryNote

                            if noteEntryNote == note and amountAccountEntryNote == amountOriginal and amountOriginal > 0:
                                return entryNote

                            if noteEntryNote == note and amountAccountEntryNote == amountPayment and amountPayment > 0:
                                return entryNote
                        else: # se não tiver a nota olha outros pontos de apoios que não são tão confiáveis
                            if issueEntryNote == ddoc_ent and cgceProviderEntryNote == cgceProvider and ddoc_ent is not None:
                                return entryNote

                            if entryEntryNote == dent_ent and cgceProviderEntryNote == cgceProvider and dent_ent is not None:
                                return entryNote

                            if issueEntryNote == dueDate and cgceProviderEntryNote == cgceProvider and dueDate is not None:
                                return entryNote
                            
                            if amountAccountEntryNote == amountOriginal and cgceProviderEntryNote == cgceProvider and amountOriginal > 0:
                                return entryNote

                            if amountAccountEntryNote == amountPayment and cgceProviderEntryNote == cgceProvider and amountPayment > 0:
                                return entryNote

                        # comparação pelo nome, caso as hipóteses acima não retorne nada
                        compareTwoWords = self.compareTwoNames(nameProviderEntryNote, nameProvider)
                        if compareTwoWords["first7LettersEquals"] is True or compareTwoWords["percentWordsEqualsAboutNameTwo"] >= 0.25:
                            if note != 0: # se a nota for válida compara os dados com ela, uma comparação no mínimo tem que ser igual, pq a se a nota tá preenchida ela tem que existir na domínio (mesmo número)
                                if noteEntryNote == note:
                                    return entryNote
                            else:
                                if issueEntryNote == ddoc_ent and ddoc_ent is not None:
                                    return entryNote

                                if entryEntryNote == dent_ent and dent_ent is not None:
                                    return entryNote

                                if issueEntryNote == dueDate and dueDate is not None:
                                    return entryNote
                                
                                if amountAccountEntryNote == amountOriginal and amountOriginal > 0:
                                    return entryNote

                                if amountAccountEntryNote == amountPayment and amountPayment > 0:
                                    return entryNote

    def returnDataInstallmentsEntryNote(self, dueDate=None, note=0, cgceProvider=None, ddoc_ent = None, dent_ent = None, amountPayment = 0.0, amountOriginal=0.0):
        if dueDate is None:
            return None # se a data de vencimento for nula já nem processa o resto

        if note == "" or note is None:
            note = 0
        if cgceProvider == "":
            cgceProvider = None
        if ddoc_ent == "":
            ddoc_ent = None
        if dent_ent == "":
            dent_ent = None

        # se o vencimento for nulo já nem percorre os dados
        if dueDate is None:
            return None

        for installment in self._installments:
            provider = self.returnDataProvider(installment["codi_for"])

            dueDateEntryNote = funcoesUteis.transformaCampoDataParaFormatoBrasileiro( \
                funcoesUteis.retornaCampoComoData(funcoesUteis.analyzeIfFieldIsValid(installment, "vcto_entp"), 2) )
            cgceProviderEntryNote = funcoesUteis.analyzeIfFieldIsValid(provider, "cgce_for", None)
            noteEntryNote = int(funcoesUteis.analyzeIfFieldIsValid(installment, "nume_ent", 0))
            issueEntryNote = funcoesUteis.transformaCampoDataParaFormatoBrasileiro( \
                funcoesUteis.retornaCampoComoData(funcoesUteis.analyzeIfFieldIsValid(installment, "ddoc_ent"), 2) )
            entryEntryNote = funcoesUteis.transformaCampoDataParaFormatoBrasileiro( \
                funcoesUteis.retornaCampoComoData(funcoesUteis.analyzeIfFieldIsValid(installment, "dent_ent"), 2) )
            amountInstallmentEntryNote = float(funcoesUteis.analyzeIfFieldIsValid(installment, "vlor_entp", 0.0))

            # o int é pra poder tirar o .0 de quando é exportado os dados
            note = funcoesUteis.treatNumberField(note, True)

            if note != 0: # se a nota for válida compara os dados com ela, uma comparação no mínimo tem que ser igual, pq a se a nota tá preenchida ela tem que existir na domínio (mesmo número)
                if dueDateEntryNote == dueDate and noteEntryNote == note:
                    return installment
            else:
                if dueDateEntryNote == dueDate and cgceProviderEntryNote == cgceProvider:
                    return installment

                if dueDateEntryNote == dueDate and issueEntryNote == ddoc_ent and ddoc_ent is not None:
                    return installment

                if dueDateEntryNote == dueDate and entryEntryNote == dent_ent and dent_ent is not None:
                    return installment

                if dueDateEntryNote == dueDate and amountInstallmentEntryNote == amountOriginal and amountOriginal > 0:
                    return installment
                    
                if dueDateEntryNote == dueDate and amountInstallmentEntryNote == amountPayment and amountPayment > 0:
                    return installment

    def process(self):
        countTotal = len(self._payments)
        for key, payment in enumerate(self._payments):
            document = funcoesUteis.analyzeIfFieldIsValid(payment, "document")
            cgceProvider = funcoesUteis.analyzeIfFieldIsValid(payment, "cgceProvider")
            cgceProvider = None if cgceProvider == "" else cgceProvider[:12] # retorna só 12 pois os dois últimos do cnpj são apenas dígitos verificadores. Já se for CPF retorna tudo
            issueDate = funcoesUteis.analyzeIfFieldIsValid(payment, "issueDate", None)
            dueDate = funcoesUteis.analyzeIfFieldIsValid(payment, "dueDate", None)
            amountPaid = funcoesUteis.analyzeIfFieldIsValid(payment, "amountPaid", 0.0)
            amountOriginal = funcoesUteis.analyzeIfFieldIsValid(payment, "amountOriginal", 0.0)
            nameProvider = funcoesUteis.analyzeIfFieldIsValid(payment, "nameProvider", None)
            
            entryNote = self.returnDataEntryNote(document, cgceProvider, issueDate, issueDate, amountPaid, nameProvider)
            if entryNote is None:
                installmentsEntryNote = self.returnDataInstallmentsEntryNote(dueDate, document, cgceProvider, issueDate, issueDate, amountPaid, amountOriginal)
                codi_for = funcoesUteis.analyzeIfFieldIsValid(installmentsEntryNote, "codi_for", 0)
            else:
                codi_for = funcoesUteis.analyzeIfFieldIsValid(entryNote, "codi_for", 0)

            if entryNote is not None:
                payment["findNote"] = True
            else:
                payment["findNote"] = False

            provider = self.returnDataProvider(codi_for)
            
            if provider is None:
                provider = self.returnDataProvider(cgce=cgceProvider, name=nameProvider)

            accountCode = funcoesUteis.analyzeIfFieldIsValid(provider, "codi_cta", 0)
            accountCode = 0 if accountCode is None else int(accountCode)
            payment["accountCode"] = accountCode
            payment["codiEmp"] = self._codiEmp
            payment["nameProvider"] = funcoesUteis.analyzeIfFieldIsValid(provider, "nome_for") if nameProvider is None or nameProvider == "" else nameProvider

            if document == "":
                payment["document"] = int(funcoesUteis.analyzeIfFieldIsValid(entryNote, "nume_ent", 0))
            
            if cgceProvider == "":
                payment["cgceProvider"] = funcoesUteis.analyzeIfFieldIsValid(provider, "cgce_for_original")

            print(f' \t - Processamento pagamento {key+1} de {countTotal}')
            
            self._paymentsFinal.append(payment)

        return self._paymentsFinal

# if __name__ == "__main__":
    # providers = [ {'codi_for': 531, 'nome_for': 'FORNECEDORES DIVERSOS', 'nomr_for': 'DIVERSOS', 'cgce_for': '33333333000191', 'codi_cta': 1004.0, 'insc_for': None, 'imun_for': None, 'codigo_municipio': 977, 'sigl_est': 'GO', 'conta_cliente_for': None, 'conta_compensacao_for': None}, {'codi_for': 536, 'nome_for': 'WALSYWA INDUSTRIA E COMERCIO DE PRODUTOS', 'nomr_for': 'WALSYWA INDUSTRIA E COMERCIO DE PRODUTOS', 'cgce_for': '05896435000503', 'codi_cta': 1009.0, 'insc_for': '421086370113', 'imun_for': None, 'codigo_municipio': 5091, 'sigl_est': 'SP', 'conta_cliente_for': None, 'conta_compensacao_for': None}]
    # entryNotes = [{'codi_emp': 1428, 'codi_ent': 3517, 'nume_ent': 135610.0, 'codi_for': 536, 'nome_for': 'WALSYWA INDUSTRIA E COMERCIO DE PRODUTOS', 'codi_esp': 36, 'codi_acu': 6, 'codi_nat': 2102, 'segi_ent': 0, 'seri_ent': '1', 'dent_ent': '2019-10-09T00:00:00.000Z', 'ddoc_ent': '2019-09-30T00:00:00.000Z', 'vcon_ent': 6040.5}, {'codi_emp': 1428, 'codi_ent': 3518, 'nume_ent': 135744.0, 'codi_for': 597, 'nome_for': 'SECURITY SYSTEMS SOLUTIONS COMERCIAL LTD', 'codi_esp': 36, 'codi_acu': 6, 'codi_nat': 2102, 'segi_ent': 0, 'seri_ent': '1', 'dent_ent': '2019-10-09T00:00:00.000Z', 'ddoc_ent': '2019-09-30T00:00:00.000Z', 'vcon_ent': 11303.1}]
    # payments = [{'paymentDate': '30/10/2019', 'nameProvider': 'WALSYWA INDUSTRIA E COMERCIO D', 'cnpjProvider': '', 'amountPaid': 2340.5, 'bank': 'ITAU', 'account': '44388', 'document': '135610', 'historic': 'VLR. REF. COMPRAS CF. NF. NUM. 135610 -', 'amountDiscount': 0.0, 'amountInterest': 0.0, 'amountOriginal': 2340.5, 'accountPlan': 'COMPRA MERCADORIA', 'bankCheck': '', 'dateExtract': '', 'bankExtract': '', 'accountExtract': '', 'historicExtract': ''}]
# #     # print(entryNotes)
    # comparePaymentsFinalWithDataBase = ComparePaymentsFinalWithDataBase()
    # print(comparePaymentsFinalWithDataBase.returnDataProvider())
    # print(comparePaymentsFinalWithDataBase.compareTwoNames('ELDER VIVOT DIAS', 'ELDER VIVOT'))
#     # print(comparePaymentsFinalWithDataBase.returnDataProvider(name="WALSYWA INDUSTRIA E COMERCIO D", degreeOfReliability=1))
#     print(comparePaymentsFinalWithDataBase.returnDataEntryNote("135610", None, None, None, 2340.5, "WALSYWA INDUSTRIA E COMERCIO"))
#     # print(comparePaymentsFinalWithDataBase.process())