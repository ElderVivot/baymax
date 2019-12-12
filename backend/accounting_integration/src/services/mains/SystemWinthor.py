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

wayToSaveFiles = open(os.path.join(fileDir, 'backend/accounting_integration/src/WayToSaveFiles.json') )
wayDefault = json.load(wayToSaveFiles)
wayToSaveFiles.close()


class SystemWinthor(object):
    def __init__(self):
        self._payments = []
        self._paymentsDates = []
        self._proofsOfPayments = []
        self._extracts = []
        self._codiEmp = input(f'\n\n- Digite o código da empresa dentro da Domínio que será realizada a integração: ')
        self._dateInicial = input(f'\n\n- Informe a data inicial (dd/mm/aaaa): ')
        self._dateFinal = input(f'- Informe a data final (dd/mm/aaaa): ')
        # self._codiEmp = 1428
        self._wayFilesToRead = os.path.join(wayDefault['WayToSaveFilesOriginals'], f'{self._codiEmp}/arquivos_originais')
        self._wayFilesTemp = os.path.join(fileDir, f'backend/accounting_integration/data/temp/{self._codiEmp}')

    def processesIntegration(self):
        try:
            shutil.rmtree(self._wayFilesTemp)
        except OSError as e:
            print (f"Error: {e.filename}, {e.strerror}")

        # read files originals
        print('\n\n - Etapa 1: Lendo os arquivos originais tais como extratos, planilhas do Excel.')
        for root, dirs, files in os.walk(self._wayFilesToRead):
            for file in files:
                wayFile = os.path.join(root, file)

                # extracts
                if file.lower().endswith(('.ofx', '.ofc')):
                    extractOFX = ExtractsOFX()
                    self._extracts.append(extractOFX.process(wayFile))
                # split pdfs em one page each
                elif file.lower().endswith(('.pdf')):
                    leArquivos.splitPdfOnePageEach(wayFile, self._wayFilesTemp)
                elif file.lower().endswith(('.xlsx')):
                    sispagItauExcel = SispagItauExcel(wayFile)
                    if sispagItauExcel.isSispagItauExcel():
                        self._proofsOfPayments.append(sispagItauExcel.process())

        # transform pdfs to text
        print(' - Etapa 2: Transformando pra TXTs os PDFs encontrados.')
        for root, dirs, files in os.walk(self._wayFilesTemp):
            for dir_ in dirs:
                if dir_ == "pdfs":
                    wayDir = os.path.join(root, dir_)
                    for rootDir, dirsDir, filesDir in os.walk(wayDir):
                        for file in filesDir:
                            if file.lower().endswith(('.pdf')):
                                wayFile = os.path.join(rootDir, file)
                                wayDirFile = os.path.dirname(wayFile)
                                leArquivos.PDFToText(wayFile, wayDirFile)
                    
        # reads the txts
        print(' - Etapa 3: Lendo os TXTs e analisando a estrutura deles.')
        for root, dirs, files in os.walk(self._wayFilesTemp):
            for dir_ in dirs:
                if dir_ == "pdfs":
                    wayDir = os.path.join(root, dir_)
                    for rootDir, dirsDir, filesDir in os.walk(wayDir):
                        for file in filesDir:
                            if file.lower().endswith(('.txt')):
                                wayFile = os.path.join(rootDir, file)
                                wayDirFile = os.path.dirname(wayFile)
                                
                                paymentsWinthorPDF = PaymentsWinthorPDF(wayFile)
                                if paymentsWinthorPDF.isPaymentWinthorPDF():
                                    self._paymentsDates.append(paymentsWinthorPDF.returnPaymentsDates())

        paymentsDates = funcoesUteis.removeAnDictionaryFromWithinArray(self._paymentsDates)
        
        print(' - Etapa 4: Lendo a planilha de contas do cliente e unindo a data de pagamento com o PDF de contas pagas')
        for root, dirs, files in os.walk(self._wayFilesToRead):
            for file in files:
                wayFile = os.path.join(root, file)

                if file.lower().endswith(('.xls', '.xlsx')):
                    paymentsWinthorExcel = PaymentsWinthorExcel(self._codiEmp)
                    self._payments.append(paymentsWinthorExcel.processPayments(wayFile, paymentsDates))

        print(' - Etapa 5: Separando o Financeiro, Extratos e Comprovantes de Pagamentos.')
        extracts = funcoesUteis.removeAnArrayFromWithinAnother(self._extracts)
        payments = funcoesUteis.removeAnArrayFromWithinAnother(self._payments)
        proofOfPayments = funcoesUteis.removeAnArrayFromWithinAnother(self._proofsOfPayments)
        # print(proofOfPayments)

        print(' - Etapa 6: Unindo o Financeiro com os Comprovantes de Pagamentos.')
        comparePaymentsAndProofWithExtracts = ComparePaymentsAndProofWithExtracts(extracts, payments, proofOfPayments)
        paymentsCompareWithProofAndExtracts = comparePaymentsAndProofWithExtracts.comparePaymentsFinalWithExtract()
        # print(paymentsCompareWithProofAndExtracts)

        print(' - Etapa 7: Buscando a conta do fornecedor/despesa dentro do sistema.')
        providers = leArquivos.readJson(os.path.join(fileDir, f'backend/extract/data/fornecedores/{self._codiEmp}-effornece.json'))
        entryNotes = leArquivos.readJson(os.path.join(fileDir, f'backend/extract/data/entradas/{self._codiEmp}-efentradas.json'))
        comparePaymentsFinalWithDataBase = ComparePaymentsFinalWithDataBase(providers, entryNotes, paymentsCompareWithProofAndExtracts, self._codiEmp)
        paymentsFinal = comparePaymentsFinalWithDataBase.process()
        
        print(' - Etapa 8: Exportando informações')
        generateExcel = GenerateExcel(self._codiEmp)
        generateExcel.sheetPayments(paymentsFinal)
        generateExcel.sheetExtract(extracts)
        generateExcel.closeFile()


if __name__ == "__main__":
    systemWinthor = SystemWinthor()
    systemWinthor.processesIntegration()