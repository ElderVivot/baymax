import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import json
import shutil

import tools.funcoesUteis as funcoesUteis
from tools.leArquivos import leXls_Xlsx
import tools.leArquivos as leArquivos

envData = leArquivos.readJson(os.path.join(fileDir, 'backend/env.json'))
folderToSaveFilesAccountIntegration = envData['folderToSaveFilesAccountIntegration']


class CompareWithSettings(object):

    def __init__(self, codiEmp, payments=[], extracts=[], updateOrExtract=False):
        self._updateOrExtract = updateOrExtract
        self._payments = payments
        self._paymentsWithNewAccountCode = []
        self._extracts = extracts
        self._extractsWithNewAccountCode = []
        self._codiEmp = codiEmp
        self._valuesOfLineProviderOrExpense = {}
        self._valuesOfFileProviderOrExpense = []
        self._posionsOfHeaderProviderOrExpense = {}
        self._valuesOfLineBanks = {}
        self._valuesOfFileBanks = []
        self._posionsOfHeaderBanks = {}
        self._valuesOfLineExtracts = {}
        self._valuesOfFileExtracts = []
        self._posionsOfHeaderExtracts = {}
        self._valuesFromToAccounts = {}
        self._posionsOfHeaderFromToAccounts = {}
        self._valuesAccountAndHistoricOthers = {}
        self._posionsOfHeaderAccountAndHistoricOthers = {}
        self._settingsFieldComparation = {
            "FORNECEDOR": 1,
            "PLANO DE CONTAS": 2,
            "CATEGORIA": 3,
            "HISTORICO": 4
        }
        self._settingsTypeComparation = {
            "FOR IGUAL": 1,
            "CONTER AS PALAVRAS": 2
        }
        self._settingsFieldComparationExtract = {
            "HISTORICO": 1
        }
        self._settingsOperationComparation = {
            "SOMA": "+",
            "SUBTRAI": "-"
        }
        self._wayFileDefaultSettings = os.path.join(fileDir, f'backend/accounting_integration/data/configuracoes.xlsx')
        self._wayFileSettings = os.path.join(folderToSaveFilesAccountIntegration, f'{self._codiEmp}/configuracoes_{self._codiEmp}.xlsx')
        if os.path.exists(self._wayFileSettings) is False:
            shutil.copyfile(self._wayFileDefaultSettings, self._wayFileSettings)

        # chama as funções que carregam os dados
        self.getSettingsProviderOrExpense()
        self.getSettingsBanks()
        self.getSettingsExtract()
        self.getSettingsFromToOfAccounts()
        self.getSettingsAccountAndHistoricOthers()
        
    def getSettingsProviderOrExpense(self):
        dataFile = leXls_Xlsx(self._wayFileSettings, 'FornecedorOuDespesa')
        
        for data in dataFile:
            try:
                if str(data[0]).upper().count('QUANDO NO CAMPO') > 0:
                    self._posionsOfHeaderProviderOrExpense.clear()
                    for keyField, nameField in enumerate(data):
                        nameField = funcoesUteis.treatTextField(nameField)
                        self._posionsOfHeaderProviderOrExpense[nameField] = keyField
                    continue
                
                fieldComparation = funcoesUteis.treatTextFieldInVector(data, 1, self._posionsOfHeaderProviderOrExpense, "Quando no Campo")
                fieldComparation = self._settingsFieldComparation[fieldComparation]

                typeComparation = funcoesUteis.treatTextFieldInVector(data, 2, self._posionsOfHeaderProviderOrExpense, "Tipo comparação")
                typeComparation = self._settingsTypeComparation[typeComparation]

                valueComparation = funcoesUteis.treatTextFieldInVector(data, 3, self._posionsOfHeaderProviderOrExpense, "Valor")

                accountDominio = int(funcoesUteis.treatNumberFieldInVector(data, 4, self._posionsOfHeaderProviderOrExpense, "Conta Contábil Domínio"))

                overwriteAccount = funcoesUteis.treatTextFieldInVector(data, 5, self._posionsOfHeaderProviderOrExpense, "Sobrescrever a Conta na Planilha Processada?")

                if fieldComparation != "" and valueComparation != "" and accountDominio > 0:
                    self._valuesOfLineProviderOrExpense = {
                        "fieldComparation": fieldComparation,
                        "typeComparation": typeComparation,
                        "valueComparation": valueComparation,
                        "accountDominio": accountDominio,
                        "overwriteAccount": overwriteAccount
                    }

                    self._valuesOfFileProviderOrExpense.append(self._valuesOfLineProviderOrExpense.copy())
            except Exception as e:
                pass

        return self._valuesOfFileProviderOrExpense

    def getSettingsBanks(self):
        dataFile = leXls_Xlsx(self._wayFileSettings, 'Bancos')
        
        for data in dataFile:
            try:
                if str(data[0]).upper().count('COMPARAR COM') > 0 or str(data[0]).upper().count('BANCO') > 0:
                    self._posionsOfHeaderBanks.clear()
                    for keyField, nameField in enumerate(data):
                        nameField = funcoesUteis.treatTextField(nameField)
                        self._posionsOfHeaderBanks[nameField] = keyField
                    continue
                
                compareWith = funcoesUteis.treatTextFieldInVector(data, 1, self._posionsOfHeaderBanks, "Comparar Com")
                compareWith = "" if compareWith != "EXTRATO BANCARIO" and compareWith != "FINANCEIRO DO CLIENTE" else compareWith

                nameBank = funcoesUteis.treatTextFieldInVector(data, 2, self._posionsOfHeaderBanks, "Banco")

                account = funcoesUteis.treatTextFieldInVector(data, 3, self._posionsOfHeaderBanks, "Conta Corrente (Sem o Dígito Verificador)")
                # account = account[:-1] # o -1 é pra tirar o digíto verificador caso o pessoal preencha na configuração, então pega sempre um char a menos evitando este problema

                accountDominio = int(funcoesUteis.treatNumberFieldInVector(data, 4, self._posionsOfHeaderBanks, "Conta Contábil Banco na Domínio"))

                if nameBank != "" and accountDominio > 0:
                    self._valuesOfLineBanks = {
                        "compareWith": compareWith,
                        "nameBankComparation": nameBank,
                        "accountComparation": account,
                        "accountDominio": accountDominio
                    }

                    self._valuesOfFileBanks.append(self._valuesOfLineBanks.copy())
            except Exception as e:
                pass
            
        return self._valuesOfFileBanks

    def getSettingsExtract(self):
        dataFile = leXls_Xlsx(self._wayFileSettings, 'ExtratoBancario')
        
        for data in dataFile:
            try:
                if str(data[0]).upper().count('QUANDO NO CAMPO') > 0:
                    self._posionsOfHeaderExtracts.clear()
                    for keyField, nameField in enumerate(data):
                        nameField = funcoesUteis.treatTextField(nameField)
                        self._posionsOfHeaderExtracts[nameField] = keyField
                    continue
                
                fieldComparation = funcoesUteis.treatTextFieldInVector(data, 1, self._posionsOfHeaderExtracts, "Quando no Campo")
                fieldComparation = self._settingsFieldComparationExtract[fieldComparation]

                operationComparation = funcoesUteis.treatTextFieldInVector(data, 2, self._posionsOfHeaderExtracts, "Operação for")
                operationComparation = self._settingsOperationComparation[operationComparation]

                typeComparation = funcoesUteis.treatTextFieldInVector(data, 3, self._posionsOfHeaderExtracts, "Tipo comparação")
                typeComparation = self._settingsTypeComparation[typeComparation]

                valueComparation = funcoesUteis.treatTextFieldInVector(data, 4, self._posionsOfHeaderExtracts, "Valor")

                accountDominio = int(funcoesUteis.treatNumberFieldInVector(data, 5, self._posionsOfHeaderExtracts, "Conta Contábil Domínio"))

                if fieldComparation != "" and valueComparation != "" and accountDominio > 0:
                    self._valuesOfLineExtracts = {
                        "fieldComparation": fieldComparation,
                        "operationComparation": operationComparation,
                        "typeComparation": typeComparation,
                        "valueComparation": valueComparation,
                        "accountDominio": accountDominio
                    }

                    self._valuesOfFileExtracts.append(self._valuesOfLineExtracts.copy())
            except Exception as e:
                pass

        return self._valuesOfFileExtracts

    def getSettingsFromToOfAccounts(self):
        dataFile = leXls_Xlsx(self._wayFileSettings, 'DeParaPlanoContas')
        
        for data in dataFile:
            try:
                fieldHeader = funcoesUteis.treatTextFieldInVector(data, 1)
                if fieldHeader.count('CODIGO CONTA SISTEMA CLIENTE') > 0:
                    self._posionsOfHeaderFromToAccounts.clear()
                    for keyField, nameField in enumerate(data):
                        nameField = funcoesUteis.treatTextField(nameField)
                        self._posionsOfHeaderFromToAccounts[nameField] = keyField
                    continue
                
                valueComparation = funcoesUteis.treatTextFieldInVector(data, 1, self._posionsOfHeaderFromToAccounts, "Código Conta Sistema Cliente")

                accountDominio = int(funcoesUteis.treatNumberFieldInVector(data, 4, self._posionsOfHeaderFromToAccounts, "Conta Contábil Domínio"))

                if valueComparation != "" and accountDominio != "":
                    self._valuesFromToAccounts[valueComparation] = accountDominio
            except Exception as e:
                pass

        return self._valuesFromToAccounts

    def getSettingsAccountAndHistoricOthers(self):
        dataFile = leXls_Xlsx(self._wayFileSettings, 'ContasEHistoricoOutros')
        
        for data in dataFile:
            try:
                fieldHeader = funcoesUteis.treatTextFieldInVector(data, 1)
                if fieldHeader.count('QUANDO HOUVER') > 0:
                    self._posionsOfHeaderAccountAndHistoricOthers.clear()
                    for keyField, nameField in enumerate(data):
                        nameField = funcoesUteis.treatTextField(nameField)
                        self._posionsOfHeaderAccountAndHistoricOthers[nameField] = keyField
                    continue
                
                # juros, multa, desconto
                fieldComparation = funcoesUteis.treatTextFieldInVector(data, 1, self._posionsOfHeaderAccountAndHistoricOthers, "Quando houver")
                if fieldComparation == "":
                    continue

                # historico ou conta contabil
                fieldOthers = funcoesUteis.treatTextFieldInVector(data, 2, self._posionsOfHeaderAccountAndHistoricOthers, "na Domínio o código do(a)")

                valueDominio = funcoesUteis.treatNumberFieldInVector(data, 3, self._posionsOfHeaderAccountAndHistoricOthers, "Será o")

                if fieldComparation != "" and fieldOthers != "" and valueDominio != "":
                    self._valuesAccountAndHistoricOthers[fieldComparation, fieldOthers] = valueDominio

                whenColumnDocumento = funcoesUteis.treatTextFieldInVector(data, 7, self._posionsOfHeaderAccountAndHistoricOthers, "Quando na Coluna Documento")

                compositionHistoric = funcoesUteis.treatTextFieldInVector(data, 8, self._posionsOfHeaderAccountAndHistoricOthers, "Composição Histórico", keepTextOriginal=False)
                
                if whenColumnDocumento != "" and compositionHistoric != "":
                    self._valuesAccountAndHistoricOthers[whenColumnDocumento] = compositionHistoric
                
            except Exception as e:
                pass

    def returnDataProviderOrExpense(self, nameProvider=None, account=None, category=None, historic=None):

        if nameProvider == "":
            nameProvider = None
        if account == "":
            account = None
        if category == "":
            category = None
        if historic == "":
            historic = None

        for providerOrExpense in self._valuesOfFileProviderOrExpense:
            fieldComparation = funcoesUteis.analyzeIfFieldIsValid(providerOrExpense, "fieldComparation")
            typeComparation = funcoesUteis.analyzeIfFieldIsValid(providerOrExpense, "typeComparation")
            valueComparation = funcoesUteis.analyzeIfFieldIsValid(providerOrExpense, "valueComparation")

            try:
                if fieldComparation == 1: # comparação pelo fornecedor
                    if typeComparation == 1: # comparação caso o valor seja idêntico
                        if nameProvider == valueComparation and nameProvider is not None:
                            return providerOrExpense
                    else:
                        if nameProvider.count(valueComparation) > 0 and nameProvider is not None: # comparação caso contenha o texto
                            return providerOrExpense
                elif fieldComparation == 2: # comparação pela conta contábil
                    if typeComparation == 1: # comparação caso o valor seja idêntico
                        if account == valueComparation and account is not None:
                            return providerOrExpense
                    else:
                        if account.count(valueComparation) > 0 and account is not None: # comparação caso contenha o texto
                            return providerOrExpense
                elif fieldComparation == 3: # comparação pela categoria
                    if typeComparation == 1: # comparação caso o valor seja idêntico
                        if category == valueComparation and category is not None:
                            return providerOrExpense
                    else:
                        if category.count(valueComparation) > 0 and category is not None: # comparação caso contenha o texto
                            return providerOrExpense
                elif fieldComparation == 4: # comparação pelo historico
                    if typeComparation == 1: # comparação caso o valor seja idêntico
                        if historic == valueComparation and historic is not None:
                            return providerOrExpense
                    else:
                        if historic.count(valueComparation) > 0 and historic is not None: # comparação caso contenha o texto
                            return providerOrExpense
            except Exception:
                pass

    def returnDataBanks(self, nameBank="", account=None, compareWith=None):

        if nameBank is None:
            nameBank = ""

        if compareWith == "":
            compareWith = None

        for bank in self._valuesOfFileBanks:
            compareWithComparation = funcoesUteis.analyzeIfFieldIsValid(bank, "compareWith")
            bankComparation = funcoesUteis.analyzeIfFieldIsValid(bank, "nameBankComparation").replace('-', ' ')
            accountComparation = funcoesUteis.analyzeIfFieldIsValid(bank, "accountComparation")
            accountDominio = funcoesUteis.analyzeIfFieldIsValid(bank, "accountDominio")

            if ( compareWithComparation == compareWith or compareWithComparation == "" or compareWithComparation == "FINANCEIRO OU EXTRATO" ) and nameBank.find(bankComparation) >= 0 and (account.count(accountComparation) > 0 or account == accountComparation):
                return accountDominio

    def returnDataExtract(self, historic=None, operation=None):

        if historic == "":
            historic = None
        if operation == "":
            operation = None

        for extractComparation in self._valuesOfFileExtracts:
            fieldComparation = funcoesUteis.analyzeIfFieldIsValid(extractComparation, "fieldComparation")
            operationComparation = funcoesUteis.analyzeIfFieldIsValid(extractComparation, "operationComparation")
            typeComparation = funcoesUteis.analyzeIfFieldIsValid(extractComparation, "typeComparation")
            valueComparation = funcoesUteis.analyzeIfFieldIsValid(extractComparation, "valueComparation")
            accountDominio = funcoesUteis.analyzeIfFieldIsValid(extractComparation, "accountDominio")

            if fieldComparation == 1: # comparação pelo fornecedor
                if typeComparation == 1: # comparação caso o valor seja idêntico
                    if historic is not None and historic == valueComparation and operationComparation == operation:
                        return accountDominio
                else:
                    if historic is not None and historic.count(valueComparation) > 0 and operationComparation == operation: # comparação caso contenha o texto
                        return accountDominio

    def showWarningsPayments(self, payment, key):
        accountCodeDebit = funcoesUteis.treatNumberField(funcoesUteis.analyzeIfFieldIsValid(payment, "accountCode"), isInt=True)
        accountCodeCredit = funcoesUteis.treatNumberField(funcoesUteis.analyzeIfFieldIsValid(payment, "accountCodeBank", 0), isInt=True)
        if accountCodeDebit == 0:
            print(f"\t\t - Na planilha de Pagamentos na linha {key+2} não foi configurado a conta do fornecedor/despesa.")
        if accountCodeCredit == 0:
            print(f"\t\t - Na planilha de Pagamentos na linha {key+2} não foi configurado a conta do banco.")

    def showWarningsExtracts(self, extract, key):
        accountCodeDebit = funcoesUteis.treatNumberField(funcoesUteis.analyzeIfFieldIsValid(extract, "accountCodeDebit"), isInt=True)
        accountCodeCredit = funcoesUteis.treatNumberField(funcoesUteis.analyzeIfFieldIsValid(extract, "accountCodeCredit"), isInt=True)
        
        foundProofInPayments = funcoesUteis.analyzeIfFieldIsValid(extract, "foundProofInPayments", False)
        if foundProofInPayments is True and accountCodeDebit > 0 and accountCodeCredit > 0:
            print(f"\t\t - Na planilha do ExtratoBancario na linha {key+2} existe a informação que é uma transação que tem no financeiro do cliente, todavia foi inserido pra importá-la também no extrato.")
            
        operation = funcoesUteis.analyzeIfFieldIsValid(extract, "operation")
        if operation == "+" and ( accountCodeDebit == 0 or accountCodeCredit == 0 ):
            print(f"\t\t - Na planilha do ExtratoBancario na linha {key+2} a operação é SOMA mas não foi configurado a conta do débito ou crédito.")

    def processPayments(self):
        
        for key, payment in enumerate(self._payments):
            document = funcoesUteis.analyzeIfFieldIsValid(payment, "document", None)
            nameProvider = funcoesUteis.analyzeIfFieldIsValid(payment, "nameProvider", None)
            accountPlan = funcoesUteis.analyzeIfFieldIsValid(payment, "accountPlan", None)
            category = funcoesUteis.analyzeIfFieldIsValid(payment, "category", None)
            historic = funcoesUteis.analyzeIfFieldIsValid(payment, "historic", None)
            bank = funcoesUteis.analyzeIfFieldIsValid(payment, "bank", None)
            account = funcoesUteis.analyzeIfFieldIsValid(payment, "account")

            # busca a conta da despesa/fornecedor
            accountCode = funcoesUteis.treatNumberField(funcoesUteis.analyzeIfFieldIsValid(payment, "accountCode", 0), isInt=True)
            dataProviderOrExpense = self.returnDataProviderOrExpense(nameProvider, accountPlan, category, historic)
            accountCodeNew = funcoesUteis.analyzeIfFieldIsValid(dataProviderOrExpense, 'accountDominio', None)
            overwriteAccount = funcoesUteis.analyzeIfFieldIsValid(dataProviderOrExpense, 'overwriteAccount', '')
            if overwriteAccount == 'SIM':
                accountCode = 0 if accountCodeNew is None else accountCodeNew
            else:
                if accountCode == 0:
                    accountCode = 0 if accountCodeNew is None else accountCodeNew
            
            # pra empresas que tem plano de contas no sistema deles e o plano não bate, tem que fazer um de-para
            accountCodeOld = funcoesUteis.analyzeIfFieldIsValid(payment, "accountCodeOld", None)
            if accountCode == 0 and accountCodeOld != "" and accountCodeOld is not None:
                accountCode = funcoesUteis.treatNumberField(funcoesUteis.analyzeIfFieldIsValid(self._valuesFromToAccounts, accountCodeOld, None), isInt=True)
                accountCode = 0 if accountCode is None else accountCode

            accountCodeBank = self.returnDataBanks(bank, account, 'FINANCEIRO DO CLIENTE')
                
            payment["accountCode"] = accountCode
            payment["accountCodeBank"] = accountCodeBank

            # print(self._valuesAccountAndHistoricOthers)
            payment["historicCodeDiscount"] = funcoesUteis.returnDataFieldInDict(self._valuesAccountAndHistoricOthers, [("DESCONTO", "HISTORICO")], 0)
            payment["historicCodeInterest"] = funcoesUteis.returnDataFieldInDict(self._valuesAccountAndHistoricOthers, [("JUROS", "HISTORICO")], 0)
            payment["historicCodeFine"] = funcoesUteis.returnDataFieldInDict(self._valuesAccountAndHistoricOthers, [("MULTA", "HISTORICO")], 0)
            payment["historicCodePagamento"] = funcoesUteis.returnDataFieldInDict(self._valuesAccountAndHistoricOthers, [("PAGAMENTO", "HISTORICO")], 0)
            payment["accountCodeDiscount"] = funcoesUteis.returnDataFieldInDict(self._valuesAccountAndHistoricOthers, [("DESCONTO", "CONTA CONTABIL")], 434)
            payment["accountCodeInterest"] = funcoesUteis.returnDataFieldInDict(self._valuesAccountAndHistoricOthers, [("JUROS", "CONTA CONTABIL")], 372)
            payment["accountCodeFine"] = funcoesUteis.returnDataFieldInDict(self._valuesAccountAndHistoricOthers, [("MULTA", "CONTA CONTABIL")], 352)
            
            compositionHistoricPrimeiraPalavraNumero = funcoesUteis.analyzeIfFieldIsValid(self._valuesAccountAndHistoricOthers, "PRIMEIRA PALAVRA E UM NUMERO")
            compositionHistoricPrimeiraPalavraNaoNumero = funcoesUteis.analyzeIfFieldIsValid(self._valuesAccountAndHistoricOthers, "PRIMEIRA PALAVRA NAO E UM NUMERO")
            compositionHistoricDiferenteVazio = funcoesUteis.analyzeIfFieldIsValid(self._valuesAccountAndHistoricOthers, "FOR DIFERENTE DE VAZIO")
            compositionHistoricVazio = funcoesUteis.analyzeIfFieldIsValid(self._valuesAccountAndHistoricOthers, "FOR VAZIO")
            
            if document is not None and document != "":
                documentSplit = str(document).split()

                if funcoesUteis.treatNumberField(documentSplit[0], True) > 0 and compositionHistoricPrimeiraPalavraNumero != "":
                    payment["compositionHistoric"] = compositionHistoricPrimeiraPalavraNumero
                if funcoesUteis.treatNumberField(documentSplit[0], True) == 0 and compositionHistoricPrimeiraPalavraNaoNumero != "":
                    payment["compositionHistoric"] = compositionHistoricPrimeiraPalavraNaoNumero
                if document != "" and compositionHistoricDiferenteVazio != "":
                    payment["compositionHistoric"] = compositionHistoricDiferenteVazio
            else:
                payment["compositionHistoric"] = compositionHistoricVazio
            
            # print(payment)

            self._paymentsWithNewAccountCode.append(payment)

            # show de warnings
            if self._updateOrExtract is True:
                self.showWarningsPayments(payment, key)

        return self._paymentsWithNewAccountCode

    def processExtracts(self):
        
        for key, extract in enumerate(self._extracts):
            nameBank = funcoesUteis.analyzeIfFieldIsValid(extract, "bank", None)
            account = funcoesUteis.analyzeIfFieldIsValid(extract, "account", None)
            operation = funcoesUteis.analyzeIfFieldIsValid(extract, "operation", None)
            historic = funcoesUteis.analyzeIfFieldIsValid(extract, "historic", None)

            accountCodeDebit = funcoesUteis.treatNumberField(funcoesUteis.analyzeIfFieldIsValid(extract, "accountCodeDebit", 0), isInt=True)
            accountCodeCredit = funcoesUteis.treatNumberField(funcoesUteis.analyzeIfFieldIsValid(extract, "accountCodeCredit", 0), isInt=True)

            # --- retorna a conta débito/crédito referente ao banco
            accountCodeBank = self.returnDataBanks(nameBank, account, 'EXTRATO BANCARIO')
            accountCodeBank = 0 if accountCodeBank is None else accountCodeBank

            if operation == "+":
                extract["accountCodeDebit"] = "" if accountCodeBank == 0 else accountCodeBank

            if operation == "-":
                extract["accountCodeCredit"] = "" if accountCodeBank == 0 else accountCodeBank

            # --- retorna a conta débito/crédito referente a contrapartida
            accountCodeExtract = self.returnDataExtract(historic, operation)
            accountCodeExtract = 0 if accountCodeExtract is None else accountCodeExtract

            foundProofInPayments = funcoesUteis.analyzeIfFieldIsValid(extract, "foundProofInPayments", False)

            if operation == "+" and accountCodeCredit == 0:
                extract["accountCodeCredit"] = "" if accountCodeExtract == 0 else accountCodeExtract

            if operation == "-" and accountCodeDebit == 0 and foundProofInPayments is False:
                extract["accountCodeDebit"] = "" if accountCodeExtract == 0 else accountCodeExtract

            self._extractsWithNewAccountCode.append(extract)

            # show de warnings
            if self._updateOrExtract is True:
                self.showWarningsExtracts(extract, key)
        
        return self._extractsWithNewAccountCode

# if __name__ == "__main__":
#     payments = [{'paymentDate': '31/10/2019', 'nameProvider': 'SANEAGO', 'cnpjProvider': '', 'amountPaid': 311.8, 'bank': 'ITAU', 'account': '44388', 'foundProof': True, 'document': '2099407921', 'historic': 'PAGAMENTO AGUA/ESGOTO REF.MES 10/2019 -', 'amountDiscount': 0.0, 'amountInterest': 0.0, 'amountOriginal': 311.8, 'accountPlan': 'AGUA E ESGOTO', 'bankCheck': '', 'dateExtract': '', 'bankExtract': '', 'accountExtract': '', 'historicExtract': '', 'findNote': False, 'accountCode': 0, 'cgceProvider': '', 'codiEmp': '1428'}, {'paymentDate': '31/10/2019', 'nameProvider': 'SANEAGO', 'cnpjProvider': '', 'amountPaid': 311.8, 'bank': 'ITAU', 'account': '44388', 'foundProof': True, 'document': '2099407921', 'historic': 'PAGAMENTO AGUA/ESGOTO REF.MES 10/2019 -', 'amountDiscount': 0.0, 'amountInterest': 0.0, 'amountOriginal': 311.8, 'accountPlan': 'AGUA E ESGOTO', 'bankCheck': '', 'dateExtract': '', 'bankExtract': '', 'accountExtract': '', 'historicExtract': '', 'findNote': False, 'accountCode': 0, 'cgceProvider': '', 'codiEmp': '1428'}, {'paymentDate': '03/10/2019', 'nameProvider': 'SALVARO INDUSTRIA E COMERCIO D', 'cnpjProvider': '', 'amountPaid': 5250.0, 'bank': 'ITAU', 'account': '44388', 'foundProof': True, 'document': '19142', 'historic': 'VLR. REF. COMPRAS CF. NF. NUM. 19142 -', 'amountDiscount': 0.0, 'amountInterest': 0.0, 'amountOriginal': 5250.0, 'accountPlan': 'COMPRA MERCADORIA', 'bankCheck': '', 'dateExtract': '', 'bankExtract': '', 'accountExtract': '', 'historicExtract': '', 'findNote': True, 'accountCode': 1158.0, 'cgceProvider': '80142250000103', 'codiEmp': '1428'}]
#     extracts = [{'bankId': 'ITAU', 'account': '4372443889', 'typeTransaction': 'DEBIT', 'dateTransaction': '01/10/2019', 'amount': 6500.0, 'operation': '-', 'document': '20191001001', 'historic': 'INT TED 759316'}]
#     compareWithSettings = CompareWithSettings(1428, payments, extracts)
#     print(compareWithSettings.processExtracts())