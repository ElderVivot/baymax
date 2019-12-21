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
from read_files.PaymentsWinthor import PaymentsWinthorPDF, PaymentsWinthorExcel
from read_files.ProofsPaymentsItau import ProofsPaymentsItau, SispagItauExcel
from read_files.ExtractsOFX import ExtractsOFX
from rules.ComparePaymentsAndProofWithExtracts import ComparePaymentsAndProofWithExtracts
from rules.ComparePaymentsFinalWithDataBase import ComparePaymentsFinalWithDataBase
from rules.GenerateExcel import GenerateExcel
from rules.FilterPeriod import FilterPeriod
from rules.CompareWithSettings import CompareWithSettings

wayToSaveFiles = open(os.path.join(fileDir, 'backend/accounting_integration/src/WayToSaveFiles.json') )
wayDefault = json.load(wayToSaveFiles)
wayToSaveFiles.close()


class SystemWinthor(object):
    def __init__(self):
        self._payments = []
        self._paymentsDates = []
        self._proofsOfPayments = []
        self._extracts = []
        # self._codiEmp = input(f'\n - Digite o código da empresa dentro da Domínio que será realizada a integração: ')
        # self._inicialDate = input(f'\n - Informe a data inicial (dd/mm/aaaa): ')
        # self._finalDate = input(f' - Informe a data final (dd/mm/aaaa): ')
        self._codiEmp = 890
        self._inicialDate = '01/11/2019'
        self._finalDate = '30/11/2019'
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

        self._wayFilesRead = os.path.join(self._wayFilesTemp, 'FilesReads.json')
        if os.path.exists(self._wayFilesRead) is False:
            with open(self._wayFilesRead, 'w') as fileRead:
                json.dump({}, fileRead)

    def processesIntegration(self):
        sequential = 0 # este sequencial serve pra caso tenha 2 pdfs com mesmo nome em pasta diferentes ele não sobrescreva um ao outro, portanto vai salvar com o nome - sequencial
            
        # read files originals
        print('\n - Etapa 1: Lendo os arquivos originais tais como extratos e PDFs.')
        for root, dirs, files in os.walk(self._wayFilesToRead):
            for file in files:

                wayFile = os.path.join(root, file)

                # extracts
                if file.lower().endswith(('.ofx', '.ofc')):
                    extractOFX = ExtractsOFX()
                    self._extracts.append(extractOFX.process(wayFile))
                # split pdfs em one page each
                elif file.lower().endswith(('.pdf')):
                    sequential += 1
                    leArquivos.splitPdfOnePageEach(wayFile, self._wayFilesTemp, sequential)

        # transform pdfs to text
        print(' - Etapa 2: Transformando pra TXTs os PDFs encontrados.')
        for root, dirs, files in os.walk(self._wayFilesTemp):
            for dir_ in dirs:
                if dir_ == "pdfs":
                    wayDir = os.path.join(root, dir_)
                    for rootDir, dirsDir, filesDir in os.walk(wayDir):
                        nameFileSplit = rootDir.split('\\')[-1].split('-')
                        nameFile = '.'.join(nameFileSplit[:-1])
                        if nameFile != "":
                            print(f' \t - Transformando o arquivo "{nameFile}.pdf"')
                        for file in filesDir:
                            if file.lower().endswith(('.pdf')):
                                wayFile = os.path.join(rootDir, file)
                                wayDirFile = os.path.dirname(wayFile)
                                leArquivos.PDFToText(wayFile, wayDirFile)
                    
        # reads the txts
        print(' - Etapa 3: Lendo os TXTs e analisando a estrutura deles.')
        proofsPaymentsItau = ProofsPaymentsItau(self._wayFilesTemp)
        self._proofsOfPayments.append(proofsPaymentsItau.processAll())
        
        print(' - Etapa 4: Separando o Financeiro, Extratos e Comprovantes de Pagamentos.')
        extracts = funcoesUteis.removeAnArrayFromWithinAnother(self._extracts)
        payments = funcoesUteis.removeAnArrayFromWithinAnother(self._payments)
        proofOfPayments = funcoesUteis.removeAnArrayFromWithinAnother(self._proofsOfPayments)

        print(' - Etapa 5: Comparação entre o Financeiro com os Comprovantes de Pagamentos e Extratos.')
        comparePaymentsAndProofWithExtracts = ComparePaymentsAndProofWithExtracts(extracts, payments, proofOfPayments)
        paymentsCompareWithProofAndExtracts = comparePaymentsAndProofWithExtracts.comparePaymentsFinalWithExtract()
        extractsCompareWithProofAndExtracts = comparePaymentsAndProofWithExtracts.analyseIfExtractIsInPayment()
        # # print(paymentsCompareWithProofAndExtracts)

        print(' - Etapa 6: Buscando a conta do fornecedor/despesa dentro do sistema.')
        providers = leArquivos.readJson(os.path.join(fileDir, f'backend/extract/data/fornecedores/{self._codiEmp}-effornece.json'))
        entryNotes = leArquivos.readJson(os.path.join(fileDir, f'backend/extract/data/entradas/{self._codiEmp}-efentradas.json'))
        installmentsEntryNote = leArquivos.readJson(os.path.join(fileDir, f'backend/extract/data/entradas_parcelas/{self._codiEmp}-efentradaspar.json'))
        comparePaymentsFinalWithDataBase = ComparePaymentsFinalWithDataBase(providers, entryNotes, installmentsEntryNote, paymentsCompareWithProofAndExtracts, self._codiEmp)
        paymentsFinal = comparePaymentsFinalWithDataBase.process()
        
        print(' - Etapa 7: Filtrando os pagamentos do período informado.')
        filterPeriod = FilterPeriod(self._inicialDate, self._finalDate, paymentsFinal, extractsCompareWithProofAndExtracts)
        extractsWithFilter = filterPeriod.filterExtracts()
        paymentsWithFilter = filterPeriod.filterPayments()
        # print(f'\t - Com o filtro aplicado de {len(paymentsFinal)} sobraram {len(paymentsWithFilter)}')

        print(' - Etapa 8: Configurando as contas contábeis de acordo planilha de configuracoes preenchida.')
        compareWithSettings = CompareWithSettings(self._codiEmp, paymentsWithFilter, extractsWithFilter)
        extractsCompareWithSettings = compareWithSettings.processExtracts()
        paymentsCompareWithSettings = compareWithSettings.processPayments()
        print(paymentsCompareWithSettings)

        print(' - Etapa 9: Exportando informações')
        generateExcel = GenerateExcel(self._codiEmp)
        generateExcel.sheetPayments(paymentsCompareWithSettings)
        generateExcel.sheetExtract(extractsCompareWithSettings)
        generateExcel.closeFile()
        
        print(' - Processo Finalizado.')
        # os.system('pause > nul')


if __name__ == "__main__":
    systemWinthor = SystemWinthor()
    systemWinthor.processesIntegration()