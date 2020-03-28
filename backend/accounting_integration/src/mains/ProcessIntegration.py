# coding: utf-8

import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))
sys.path.append(os.path.join(fileDir, 'backend/accounting_integration/src'))

import shutil
import json
import tools.leArquivos as leArquivos
import tools.funcoesUteis as funcoesUteis
from services.read_files.ExtractsOFX import ExtractsOFX
from services.read_files.ReadPDFs import ReadPDFs
from services.read_files.CallReadFilePayments import CallReadFilePayments
from services.read_files.CallReadFileProofs import CallReadFileProofs
from services.read_files.ReadGeneral import ReadGeneral
from services.rules.ComparePaymentsAndProofWithExtracts import ComparePaymentsAndProofWithExtracts
from services.rules.ComparePaymentsFinalWithDataBase import ComparePaymentsFinalWithDataBase
from services.rules.GenerateExcel import GenerateExcel
from services.rules.FilterPeriod import FilterPeriod
from services.rules.CompareWithSettings import CompareWithSettings
from services.rules.ReturnFilesDontFindForm import ReturnFilesDontFindForm
from dao.src.GetSettingsCompany import GetSettingsCompany

wayToSaveFiles = open(os.path.join(fileDir, 'backend/accounting_integration/src/WayToSaveFiles.json') )
wayDefault = json.load(wayToSaveFiles)
wayToSaveFiles.close()


class ProcessIntegration(object):
    def __init__(self):
        self._payments = []
        self._paymentsDates = []
        self._proofsOfPayments = []
        self._extracts = []
        self._codiEmp = int(input(f'\n - Digite o código da empresa dentro da Domínio que será realizada a integração: '))
        self._inicialDate = input(f'\n - Informe a data inicial (dd/mm/aaaa): ')
        self._finalDate = input(f' - Informe a data final (dd/mm/aaaa): ')
        # self._codiEmp = 1117
        # self._inicialDate = '01/01/2020'
        # self._finalDate = '31/01/2020'
        self._waySettings = os.path.join(fileDir, f'backend/accounting_integration/data/settings/company{self._codiEmp}.json')
        if os.path.exists(self._waySettings) is False:
            getSettingsCompany = GetSettingsCompany(self._codiEmp)
            self._settings = getSettingsCompany.getSettingsFinancy()
            self._banksToProof = funcoesUteis.returnDataFieldInDict(self._settings, ["financy", "banks", "listNumbers"], [0])
        else:
            self._settings = leArquivos.readJson(self._waySettings)
            self._banksToProof = funcoesUteis.returnDataFieldInDict(self._settings, ["banks", "listNumbers"], [0])

        self._wayFilesToRead = os.path.join(wayDefault['WayToSaveFilesOriginals'], f'{self._codiEmp}/arquivos_originais')
        self._wayFilesTemp = os.path.join(fileDir, f'backend/accounting_integration/data/temp/{self._codiEmp}')
        if os.path.exists(self._wayFilesTemp) is False:
            os.makedirs(self._wayFilesTemp)
            
        try:
            shutil.rmtree(self._wayFilesTemp)
        except OSError as e:
            print (f"Error: {e.filename}, {e.strerror}")

        if os.path.exists(self._wayFilesTemp) is False:
            os.makedirs(self._wayFilesTemp)

        self._wayReadFiles = os.path.join(self._wayFilesTemp, 'FilesReads.json')
        if os.path.exists(self._wayReadFiles) is False:
            with open(self._wayReadFiles, 'w') as fileRead:
                json.dump({}, fileRead)

    def process(self):
            
        print('\n - Etapa 1: Lendo os PDFs')
        readPDFs = ReadPDFs(self._codiEmp, self._wayFilesTemp, self._wayFilesToRead)
        readPDFs.processSplitPdfOnePageEach()
        readPDFs.transformPDFToText()
        readPDFs.doBackupFolderPDF() # faz o bkp pra não perder os dados quando apagar as informações

        # reads the txts
        print(' - Etapa 2: Lendo os OFXs ')
        extractsOFX = ExtractsOFX(self._wayFilesToRead)
        self._extracts.append(extractsOFX.processAll())

        # reads the financy
        print(' - Etapa 3: Lendo o financeiro do cliente')
        hasFinancy = funcoesUteis.returnDataFieldInDict(self._settings, ["financy", "has"])
        if hasFinancy is True:
            systemFinancy = funcoesUteis.returnDataFieldInDict(self._settings, ["financy", "system"])
            if systemFinancy == "":
                readGeneral = ReadGeneral(self._codiEmp, self._wayFilesToRead, self._settings)
                readGeneralData = readGeneral.processAll()
                self._payments = readGeneralData[0]

                self._extracts.append(readGeneralData[1])                
            else:
                callReadFilePayments = CallReadFilePayments(systemFinancy, self._codiEmp, self._wayFilesToRead, self._wayFilesTemp)
                self._payments = callReadFilePayments.process()
        else:
            print('\t - Cliente sem a configuração do sistema financeiro realizada (provavelmente esta empresa não possui)')

        self._extracts = funcoesUteis.removeAnArrayFromWithinAnother(self._extracts)
        
        # reads the txts
        print(' - Etapa 4: Lendo os comprovantes de pagamentos e analisando as estruturas deles.')
        callReadFileProofs = CallReadFileProofs(self._codiEmp, self._wayFilesTemp, self._wayFilesToRead, self._banksToProof)
        self._proofsOfPayments = callReadFileProofs.process()
        
        print(' - Etapa 5: Comparação entre o Financeiro com os Comprovantes de Pagamentos e Extratos.')
        comparePaymentsAndProofWithExtracts = ComparePaymentsAndProofWithExtracts(self._settings, self._extracts, self._payments, self._proofsOfPayments)
        paymentsCompareWithProofAndExtracts = comparePaymentsAndProofWithExtracts.comparePaymentsFinalWithExtract()
        extractsCompareWithProofAndExtracts = comparePaymentsAndProofWithExtracts.analyseIfExtractIsInPayment()
        # # print(paymentsCompareWithProofAndExtracts)

        print(' - Etapa 6: Filtrando os pagamentos do período informado.')
        filterPeriod = FilterPeriod(self._inicialDate, self._finalDate, paymentsCompareWithProofAndExtracts, extractsCompareWithProofAndExtracts)
        extractsWithFilter = filterPeriod.filterExtracts()
        paymentsWithFilter = filterPeriod.filterPayments()

        sequentialStep = 7

        hasOwnAccountPlan = funcoesUteis.returnDataFieldInDict(self._settings, ["financy", "hasOwnAccountPlan"])
        if hasOwnAccountPlan is False or hasOwnAccountPlan == "":
            print(f' - Etapa {sequentialStep}: Buscando a conta do fornecedor/despesa dentro do sistema.')
            providers = leArquivos.readJson(os.path.join(fileDir, f'backend/extract/data/fornecedores/{self._codiEmp}-effornece.json'))
            entryNotes = [] #leArquivos.readJson(os.path.join(fileDir, f'backend/extract/data/entradas/{self._codiEmp}-efentradas.json'))
            installmentsEntryNote = leArquivos.readJson(os.path.join(fileDir, f'backend/extract/data/entradas_parcelas/{self._codiEmp}-efentradaspar.json'))
            comparePaymentsFinalWithDataBase = ComparePaymentsFinalWithDataBase(self._codiEmp, self._finalDate, providers, entryNotes, installmentsEntryNote, paymentsWithFilter)
            paymentsFinal = comparePaymentsFinalWithDataBase.process()
            sequentialStep += 1
        else:
            paymentsFinal = paymentsWithFilter

        print(f' - Etapa {sequentialStep}: Configurando as contas contábeis de acordo planilha de configuracoes preenchida.')
        compareWithSettings = CompareWithSettings(self._codiEmp, paymentsFinal, extractsWithFilter)
        extractsCompareWithSettings = compareWithSettings.processExtracts()
        paymentsCompareWithSettings = compareWithSettings.processPayments()
        sequentialStep += 1

        print(f' - Etapa {sequentialStep}: Exportando informações')
        generateExcel = GenerateExcel(self._codiEmp)
        generateExcel.sheetPayments(paymentsCompareWithSettings)
        generateExcel.sheetExtract(extractsCompareWithSettings)
        generateExcel.closeFile()
        sequentialStep += 1

        print(f' - Etapa {sequentialStep}: Salvando arquivos que não foram lidos')
        returnFilesDontFindForm = ReturnFilesDontFindForm(self._codiEmp, self._wayFilesTemp)
        returnFilesDontFindForm.processAll()
        
        print(' - Processo Finalizado.')
        os.system('pause > nul')


if __name__ == "__main__":
    processIntegration = ProcessIntegration()
    processIntegration.process()