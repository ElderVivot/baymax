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
from read_files.PaymentsLys import PaymentsLysPorMoeda, PaymentsLysPorData
from rules.ComparePaymentsAndProofWithExtracts import ComparePaymentsAndProofWithExtracts
from rules.GenerateExcel import GenerateExcel
from rules.FilterPeriod import FilterPeriod
from rules.CompareWithSettings import CompareWithSettings

wayToSaveFiles = open(os.path.join(fileDir, 'backend/accounting_integration/src/WayToSaveFiles.json') )
wayDefault = json.load(wayToSaveFiles)
wayToSaveFiles.close()


class SystemLys(object):
    def __init__(self):
        self._paymentsData = []
        self._paymentsMoeda = []
        self._extracts = []
        self._codiEmp = input(f'\n - Digite o código da empresa dentro da Domínio que será realizada a integração: ')
        self._inicialDate = input(f'\n - Informe a data inicial (dd/mm/aaaa): ')
        self._finalDate = input(f' - Informe a data final (dd/mm/aaaa): ')
        # self._codiEmp = 1428
        self._wayFilesToRead = os.path.join(wayDefault['WayToSaveFilesOriginals'], f'{self._codiEmp}/arquivos_originais')
        self._wayFilesTemp = os.path.join(fileDir, f'backend/accounting_integration/data/temp/{self._codiEmp}')
        print(self._wayFilesTemp, os.path.exists(self._wayFilesTemp))
        if os.path.exists(self._wayFilesTemp) is False:
            os.makedirs(self._wayFilesTemp)

    def processesIntegration(self):
        try:
            shutil.rmtree(self._wayFilesTemp)
        except OSError as e:
            print (f"Error: {e.filename}, {e.strerror}")

        # read files originals
        print('\n - Etapa 1: Lendo os arquivos originais tais como extratos, planilhas do Excel.')
        for root, dirs, files in os.walk(self._wayFilesToRead):
            for file in files:

                wayFile = os.path.join(root, file)

                # extracts
                if file.lower().endswith(('.ofx', '.ofc')):
                    extractOFX = ExtractsOFX()
                    self._extracts.append(extractOFX.process(wayFile))
                elif file.lower().endswith(('.xlsx', '.xls')):
                    paymentsLysPorMoeda = PaymentsLysPorMoeda(wayFile)
                    self._paymentsMoeda.append(paymentsLysPorMoeda.process())

        paymentsMoeda = funcoesUteis.removeAnArrayFromWithinAnother(self._paymentsMoeda)
        
        print(' - Etapa 2: Unindo as duas planilhas financeiras do cliente')
        for root, dirs, files in os.walk(self._wayFilesToRead):
            for file in files:
                wayFile = os.path.join(root, file)

                if file.lower().endswith(('.xls', '.xlsx')):
                    paymentsLysPorData = PaymentsLysPorData(wayFile, paymentsMoeda)
                    self._paymentsData.append(paymentsLysPorData.process())

        print(' - Etapa 3: Separando o Financeiro, Extratos e Comprovantes de Pagamentos.')
        extracts = funcoesUteis.removeAnArrayFromWithinAnother(self._extracts)
        payments = funcoesUteis.removeAnArrayFromWithinAnother(self._paymentsData)
        proofOfPayments = []
        # print(payments)

        print(' - Etapa 4: Comparação entre o Financeiro com os Comprovantes de Pagamentos e Extratos.')
        comparePaymentsAndProofWithExtracts = ComparePaymentsAndProofWithExtracts(extracts, payments, proofOfPayments)
        paymentsFinal = comparePaymentsAndProofWithExtracts.comparePaymentsFinalWithExtract()
        # print(paymentsCompareWithProofAndExtracts)

        # retirado as linhas de baixo por enquanto pois na planilha do cliente já tem a conta contábil, além disso, tenho que implementar pra ler as notas das filiais
        # print(' - Etapa 7: Buscando a conta do fornecedor/despesa dentro do sistema.')
        # providers = leArquivos.readJson(os.path.join(fileDir, f'backend/extract/data/fornecedores/{self._codiEmp}-effornece.json'))
        # entryNotes = leArquivos.readJson(os.path.join(fileDir, f'backend/extract/data/entradas/{self._codiEmp}-efentradas.json'))
        # installmentsEntryNote = leArquivos.readJson(os.path.join(fileDir, f'backend/extract/data/entradas_parcelas/{self._codiEmp}-efentradaspar.json'))
        # comparePaymentsFinalWithDataBase = ComparePaymentsFinalWithDataBase(providers, entryNotes, installmentsEntryNote, paymentsCompareWithProofAndExtracts, self._codiEmp)
        # paymentsFinal = comparePaymentsFinalWithDataBase.process()
        
        print(' - Etapa 5: Filtrando os pagamentos do período informado.')
        filterPeriod = FilterPeriod(self._inicialDate, self._finalDate, paymentsFinal, extracts)
        extractsWithFilter = filterPeriod.filterExtracts()
        paymentsWithFilter = filterPeriod.filterPayments()
        # print(f'\t - Com o filtro aplicado de {len(paymentsFinal)} sobraram {len(paymentsWithFilter)}')

        print(' - Etapa 6: Configurando as contas contábeis de acordo planilha de configuracoes preenchida.')
        compareWithSettings = CompareWithSettings(self._codiEmp, paymentsWithFilter, extractsWithFilter)
        extractsCompareWithSettings = compareWithSettings.processExtracts()
        paymentsCompareWithSettings = compareWithSettings.processPayments()

        print(' - Etapa 7: Exportando informações')
        generateExcel = GenerateExcel(self._codiEmp)
        generateExcel.sheetPayments(paymentsCompareWithSettings)
        generateExcel.sheetExtract(extractsCompareWithSettings)
        generateExcel.closeFile()
        
        print(' - Processo Finalizado.')
        os.system('pause > nul')


if __name__ == "__main__":
    systemLys = SystemLys()
    systemLys.processesIntegration()