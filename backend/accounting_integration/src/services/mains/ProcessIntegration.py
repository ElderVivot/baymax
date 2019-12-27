# coding: utf-8

import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))
sys.path.append(os.path.join(fileDir, 'backend/accounting_integration/src/services'))

import shutil
import json
import tools.leArquivos as leArquivos
import tools.funcoesUteis as funcoesUteis
from read_files.ExtractsOFX import ExtractsOFX
from read_files.ReadPDFs import ReadPDFs
from read_files.CallReadFilePayments import CallReadFilePayments
from read_files.CallReadFileProofs import CallReadFileProofs
from rules.ComparePaymentsAndProofWithExtracts import ComparePaymentsAndProofWithExtracts
from rules.ComparePaymentsFinalWithDataBase import ComparePaymentsFinalWithDataBase
from rules.GenerateExcel import GenerateExcel
from rules.FilterPeriod import FilterPeriod
from rules.CompareWithSettings import CompareWithSettings
from rules.ReturnFilesDontFindForm import ReturnFilesDontFindForm

wayToSaveFiles = open(os.path.join(fileDir, 'backend/accounting_integration/src/WayToSaveFiles.json') )
wayDefault = json.load(wayToSaveFiles)
wayToSaveFiles.close()


class ProcessIntegration(object):
    def __init__(self):
        self._payments = []
        self._paymentsDates = []
        self._proofsOfPayments = []
        self._extracts = []
        self._codiEmp = input(f'\n - Digite o código da empresa dentro da Domínio que será realizada a integração: ')
        self._inicialDate = input(f'\n - Informe a data inicial (dd/mm/aaaa): ')
        self._finalDate = input(f' - Informe a data final (dd/mm/aaaa): ')
        # self._codiEmp = 1751
        # self._inicialDate = '01/10/2019'
        # self._finalDate = '31/10/2019'
        self._waySettings = os.path.join(fileDir, f'backend/accounting_integration/data/settings/company{self._codiEmp}.json')
        self._settings = leArquivos.readJson(self._waySettings)

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
        self._extracts = extractsOFX.processAll()

        # reads the financy
        print(' - Etapa 3: Lendo o financeiro do cliente')
        if self._settings["financy"]["has"] is True:
            systemFinancy = self._settings["financy"]["system"]
            callReadFilePayments = CallReadFilePayments(systemFinancy, self._codiEmp, self._wayFilesToRead, self._wayFilesTemp)
            self._payments = callReadFilePayments.process()
        else:
            print('\t - Cliente sem a configuração do sistema financeiro realizada (provavelmente esta empresa não possui)')

        # reads the txts
        print(' - Etapa 4: Lendo os comprovantes de pagamentos e analisando as estruturas deles.')
        callReadFileProofs = CallReadFileProofs(self._codiEmp, self._wayFilesTemp)
        self._proofsOfPayments = callReadFileProofs.process()
        
        print(' - Etapa 5: Separando o Financeiro, Extratos e Comprovantes de Pagamentos.')
        extracts = self._extracts # funcoesUteis.removeAnArrayFromWithinAnother(self._extracts)
        payments = self._payments # funcoesUteis.removeAnArrayFromWithinAnother(self._payments)
        proofOfPayments = self._proofsOfPayments # funcoesUteis.removeAnArrayFromWithinAnother(self._proofsOfPayments)

        print(' - Etapa 6: Comparação entre o Financeiro com os Comprovantes de Pagamentos e Extratos.')
        comparePaymentsAndProofWithExtracts = ComparePaymentsAndProofWithExtracts(extracts, payments, proofOfPayments)
        paymentsCompareWithProofAndExtracts = comparePaymentsAndProofWithExtracts.comparePaymentsFinalWithExtract()
        extractsCompareWithProofAndExtracts = comparePaymentsAndProofWithExtracts.analyseIfExtractIsInPayment()
        # # print(paymentsCompareWithProofAndExtracts)

        print(' - Etapa 7: Buscando a conta do fornecedor/despesa dentro do sistema.')
        providers = leArquivos.readJson(os.path.join(fileDir, f'backend/extract/data/fornecedores/{self._codiEmp}-effornece.json'))
        entryNotes = leArquivos.readJson(os.path.join(fileDir, f'backend/extract/data/entradas/{self._codiEmp}-efentradas.json'))
        installmentsEntryNote = leArquivos.readJson(os.path.join(fileDir, f'backend/extract/data/entradas_parcelas/{self._codiEmp}-efentradaspar.json'))
        comparePaymentsFinalWithDataBase = ComparePaymentsFinalWithDataBase(providers, entryNotes, installmentsEntryNote, paymentsCompareWithProofAndExtracts, self._codiEmp)
        paymentsFinal = comparePaymentsFinalWithDataBase.process()
        
        print(' - Etapa 8: Filtrando os pagamentos do período informado.')
        filterPeriod = FilterPeriod(self._inicialDate, self._finalDate, paymentsFinal, extractsCompareWithProofAndExtracts)
        extractsWithFilter = filterPeriod.filterExtracts()
        paymentsWithFilter = filterPeriod.filterPayments()
        # print(f'\t - Com o filtro aplicado de {len(paymentsFinal)} sobraram {len(paymentsWithFilter)}')

        print(' - Etapa 9: Configurando as contas contábeis de acordo planilha de configuracoes preenchida.')
        compareWithSettings = CompareWithSettings(self._codiEmp, paymentsWithFilter, extractsWithFilter)
        extractsCompareWithSettings = compareWithSettings.processExtracts()
        paymentsCompareWithSettings = compareWithSettings.processPayments()

        print(' - Etapa 10: Exportando informações')
        generateExcel = GenerateExcel(self._codiEmp)
        generateExcel.sheetPayments(paymentsCompareWithSettings)
        generateExcel.sheetExtract(extractsCompareWithSettings)
        generateExcel.closeFile()

        print(' - Etapa 11: Salvando arquivos que não foram lidos')
        returnFilesDontFindForm = ReturnFilesDontFindForm(self._codiEmp, self._wayFilesTemp)
        returnFilesDontFindForm.processAll()
        
        print(' - Processo Finalizado.')
        os.system('pause > nul')


if __name__ == "__main__":
    processIntegration = ProcessIntegration()
    processIntegration.process()