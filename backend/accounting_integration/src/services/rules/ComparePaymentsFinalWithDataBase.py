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
    
    def __init__(self, providers=[], entryNotes=[], installments=[], payments=[], codiEmp=0):
        self._providers = providers
        self._entryNotes = entryNotes
        self._payments = payments
        self._installments = installments
        self._codiEmp = codiEmp
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
    
    def removeWordsThatAreNotNames(self, name):
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

    def returnDataProvider(self, codi_for=0, cgce=None, name=None, degreeOfReliability=0):
        # caso os campos sejam vazios deixa eles como nulos
        if cgce == "":
            cgce = None
        if name == "":
            name = None

        for provider in self._providers:

            if int(provider['codi_for']) == int(codi_for):
                return provider

            if provider['cgce_for'] == cgce and cgce is not None:
                return provider

            # agora as verificações pelo nome (esta primeira tem grau alto de confiabilidade)
            if name is None:
                continue

            nameProvider = self.changeAbbreviatedWord(self.removeWordsThatAreNotNames(provider["nome_for"]))
            nameArgument = self.changeAbbreviatedWord(self.removeWordsThatAreNotNames(name))

            countNameProvider = len(nameProvider.split())
            nameProviderSplit = nameProvider.split(' ')

            def findProviderForName():
                countEqualWords = 0
                nameArgumentSplit = nameArgument.split(' ')
                for wordName in nameArgumentSplit:
                    if nameProviderSplit.count(wordName) > 0: # conta somente as palavras em comuns
                        countEqualWords += 1
                
                # se a quantidade de palavras em comuns for igual então já retorna o provider
                if countNameProvider == countEqualWords:
                    return provider
                
                if countNameProvider >= 3:
                    if floor(countNameProvider * 0.7) <= countEqualWords:
                        return provider
                else:
                    if nameProvider.count(nameArgument[0:floor(len(nameArgument)*0.75)]) > 0:
                        return provider

                # grau de confibilidade mais baixo, só deve ser usado junto com outra confirmação, como número da nota por exemplo
                if degreeOfReliability == 1:
                    if len(nameArgument) >= 10:
                        if nameProvider.count(nameArgument[0:floor(len(nameArgument)*0.30)]) > 0:
                            return provider
                    else:
                        if nameProvider.count(nameArgument[0:floor(len(nameArgument)*0.60)]) > 0:
                            return provider

            if findProviderForName() is not None:
                return provider

    def returnDataEntryNote(self, note=0, cgceProvider=None, ddoc_ent = None, dent_ent = None, amountPayment = 0.0, nameProvider=None):
        if note == "":
            note = 0
        if cgceProvider == "":
            cgceProvider = None
        if ddoc_ent == "":
            ddoc_ent = None
        if dent_ent == "":
            dent_ent = None
        if nameProvider == "":
            nameProvider = None

        for entryNote in self._entryNotes:
            provider = self.returnDataProvider(entryNote["codi_for"])

            cgceProviderEntryNote = funcoesUteis.analyzeIfFieldIsValid(provider, "cgce_for", None)
            noteEntryNote = int(funcoesUteis.analyzeIfFieldIsValid(entryNote, "nume_ent", 0))
            issueEntryNote = funcoesUteis.transformaCampoDataParaFormatoBrasileiro( \
                funcoesUteis.retornaCampoComoData(funcoesUteis.analyzeIfFieldIsValid(entryNote, "ddoc_ent"), 2) )
            entryEntryNote = funcoesUteis.transformaCampoDataParaFormatoBrasileiro( \
                funcoesUteis.retornaCampoComoData(funcoesUteis.analyzeIfFieldIsValid(entryNote, "dent_ent"), 2) )
            amountPaidEntryNote = float(funcoesUteis.analyzeIfFieldIsValid(entryNote, "vcon_ent", 0.0))

            note = int(note)

            # utilizo uma função pois foi precisar comparar o cgce duas vezes, então chamo ele nos dois casos diferentes
            def returnNote(cgceProviderSearch):
                if noteEntryNote == note and cgceProviderEntryNote == cgceProviderSearch:
                    return entryNote

                if noteEntryNote == note and issueEntryNote == ddoc_ent and ddoc_ent is not None:
                    return entryNote

                if noteEntryNote == note and entryEntryNote == dent_ent and dent_ent is not None:
                    return entryNote

                if noteEntryNote == note and amountPaidEntryNote == amountPayment and amountPayment > 0:
                    return entryNote

                if issueEntryNote == ddoc_ent and cgceProviderEntryNote == cgceProviderSearch and ddoc_ent is not None:
                    return entryNote

                if entryEntryNote == dent_ent and cgceProviderEntryNote == cgceProviderSearch and dent_ent is not None:
                    return entryNote
                
                if amountPaidEntryNote == amountPayment and cgceProviderEntryNote == cgceProviderSearch and amountPayment > 0:
                    return entryNote

            cgce_for = cgceProvider
            if returnNote(cgce_for) is not None:
                return returnNote(cgce_for)

            # busca a nota olhando pelo nome da empresa
            providerByName = self.returnDataProvider(name=nameProvider, degreeOfReliability=1)
            cgce_for = funcoesUteis.analyzeIfFieldIsValid(providerByName, "cgce_for", None)
            if returnNote(cgce_for) is not None:
                return returnNote(cgce_for)

    def returnDataInstallmentsEntryNote(self, dueDate=None, note=0, cgceProvider=None, ddoc_ent = None, dent_ent = None, amountPayment = 0.0, amountOriginal=0.0):
        if dueDate is None:
            return None # se a data de vencimento for nula já nem processa o resto

        if note == "":
            note = 0
        if cgceProvider == "":
            cgceProvider = None
        if ddoc_ent == "":
            ddoc_ent = None
        if dent_ent == "":
            dent_ent = None
        if nameProvider == "":
            nameProvider = None

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
            note = int(note)

            if dueDateEntryNote == dueDate and noteEntryNote == note:
                return installment

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
            cgceProvider = funcoesUteis.analyzeIfFieldIsValid(payment, "cgceProvider", None)
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

            provider = self.returnDataProvider(codi_for)

            #payment["findNote"] = 'False'

            if entryNote is not None:
                payment["findNote"] = True

            if provider is None:
                provider = self.returnDataProvider(cgce=cgceProvider, name=nameProvider)

            payment["accountCode"] = funcoesUteis.analyzeIfFieldIsValid(provider, "codi_cta", 0)
            payment["cgceProvider"] = funcoesUteis.analyzeIfFieldIsValid(provider, "cgce_for")
            payment["codiEmp"] = self._codiEmp

            print(f' \t - Processamento pagamento {key+1} de {countTotal}')
            
            self._paymentsFinal.append(payment)

        return self._paymentsFinal

# if __name__ == "__main__":
#     providers = [ {'codi_for': 531, 'nome_for': 'FORNECEDORES DIVERSOS', 'nomr_for': 'DIVERSOS', 'cgce_for': '33333333000191', 'codi_cta': 1004.0, 'insc_for': None, 'imun_for': None, 'codigo_municipio': 977, 'sigl_est': 'GO', 'conta_cliente_for': None, 'conta_compensacao_for': None}, {'codi_for': 536, 'nome_for': 'WALSYWA INDUSTRIA E COMERCIO DE PRODUTOS', 'nomr_for': 'WALSYWA INDUSTRIA E COMERCIO DE PRODUTOS', 'cgce_for': '05896435000503', 'codi_cta': 1009.0, 'insc_for': '421086370113', 'imun_for': None, 'codigo_municipio': 5091, 'sigl_est': 'SP', 'conta_cliente_for': None, 'conta_compensacao_for': None}]
#     entryNotes = [{'codi_emp': 1428, 'codi_ent': 3517, 'nume_ent': 135610.0, 'codi_for': 536, 'nome_for': 'WALSYWA INDUSTRIA E COMERCIO DE PRODUTOS', 'codi_esp': 36, 'codi_acu': 6, 'codi_nat': 2102, 'segi_ent': 0, 'seri_ent': '1', 'dent_ent': '2019-10-09T00:00:00.000Z', 'ddoc_ent': '2019-09-30T00:00:00.000Z', 'vcon_ent': 6040.5}, {'codi_emp': 1428, 'codi_ent': 3518, 'nume_ent': 135744.0, 'codi_for': 597, 'nome_for': 'SECURITY SYSTEMS SOLUTIONS COMERCIAL LTD', 'codi_esp': 36, 'codi_acu': 6, 'codi_nat': 2102, 'segi_ent': 0, 'seri_ent': '1', 'dent_ent': '2019-10-09T00:00:00.000Z', 'ddoc_ent': '2019-09-30T00:00:00.000Z', 'vcon_ent': 11303.1}]
#     payments = [{'paymentDate': '30/10/2019', 'nameProvider': 'WALSYWA INDUSTRIA E COMERCIO D', 'cnpjProvider': '', 'amountPaid': 2340.5, 'bank': 'ITAU', 'account': '44388', 'document': '135610', 'historic': 'VLR. REF. COMPRAS CF. NF. NUM. 135610 -', 'amountDiscount': 0.0, 'amountInterest': 0.0, 'amountOriginal': 2340.5, 'accountPlan': 'COMPRA MERCADORIA', 'bankCheck': '', 'dateExtract': '', 'bankExtract': '', 'accountExtract': '', 'historicExtract': ''}]
# #     # print(entryNotes)
#     comparePaymentsFinalWithDataBase = ComparePaymentsFinalWithDataBase(providers, entryNotes, payments)
#     # print(comparePaymentsFinalWithDataBase.returnDataProvider(name="WALSYWA INDUSTRIA E COMERCIO D", degreeOfReliability=1))
#     print(comparePaymentsFinalWithDataBase.returnDataEntryNote("135610", None, None, None, 2340.5, "WALSYWA INDUSTRIA E COMERCIO"))
#     # print(comparePaymentsFinalWithDataBase.process())