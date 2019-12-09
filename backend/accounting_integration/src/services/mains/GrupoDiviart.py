# coding: utf-8

import sys
import os

fileDir = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(os.path.join(fileDir, 'backend'))
sys.path.append(os.path.join(fileDir, 'backend/accounting_integration/src/services'))

import shutil
import tools.leArquivos as leArquivos
import tools.funcoesUteis as funcoesUteis
from read_files.PaymentsWinthor import PaymentsWinthorPDF, PaymentsWinthorExcel
from read_files.ProofsPaymentsItau import ProofsPaymentsItau, SispagItauExcel
from read_files.ExtractsOFX import ExtractsOFX
from rules.ComparePaymentsAndProofWithExtracts import ComparePaymentsAndProofWithExtracts
from rules.ComparePaymentsFinalWithDataBase import ComparePaymentsFinalWithDataBase


class GrupoDiviart(object):
    def __init__(self):
        self._payments = []
        self._paymentsDates = []
        self._proofsOfPayments = []
        self._extracts = []
        # self._codiEmp = input('- Digite o código da empresa dentro da Domínio que será realizada a integração: ')
        self._codiEmp = 1428
        self._wayFilesToRead = f"C:/integracao_contabil/{self._codiEmp}/arquivos_originais/temp"
        self._wayFilesTemp = os.path.join(fileDir, f'backend/accounting_integration/data/temp/{self._codiEmp}')

    def processesIntegration(self):
        try:
            shutil.rmtree(self._wayFilesTemp)
        except OSError as e:
            print (f"Error: {e.filename}, {e.strerror}")

        # read files originals
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
        
        for root, dirs, files in os.walk(self._wayFilesToRead):
            for file in files:
                wayFile = os.path.join(root, file)

                if file.lower().endswith(('.xls', '.xlsx')):
                    paymentsWinthorExcel = PaymentsWinthorExcel()
                    paymentsWinthorExcel.readValuesOfBank(os.path.join(fileDir, 'backend/accounting_integration/data/1428_banks.json'))
                    self._payments.append(paymentsWinthorExcel.processPayments(wayFile, paymentsDates))

        extracts = funcoesUteis.removeAnArrayFromWithinAnother(self._extracts)
        payments = funcoesUteis.removeAnArrayFromWithinAnother(self._payments)
        proofOfPayments = funcoesUteis.removeAnArrayFromWithinAnother(self._proofsOfPayments)

        comparePaymentsAndProofWithExtracts = ComparePaymentsAndProofWithExtracts(extracts, payments, proofOfPayments)
        paymentsCompareWithProofAndExtracts = comparePaymentsAndProofWithExtracts.comparePaymentsFinalWithExtract()

        providers = leArquivos.readJson(os.path.join(fileDir, f'backend/extract/data/fornecedores/{self._codiEmp}-effornece.json'))
        entryNotes = leArquivos.readJson(os.path.join(fileDir, f'backend/extract/data/entradas/{self._codiEmp}-efentradas.json'))
        print('teste')
        comparePaymentsFinalWithDataBase = ComparePaymentsFinalWithDataBase(providers, entryNotes, paymentsCompareWithProofAndExtracts)
        paymentsFinal = comparePaymentsFinalWithDataBase.process()
        print(paymentsFinal)

if __name__ == "__main__":
    grupoDiviart = GrupoDiviart()
    grupoDiviart.processesIntegration()
