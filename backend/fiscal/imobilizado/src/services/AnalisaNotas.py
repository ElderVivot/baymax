import sys
import os

fileDir = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(os.path.join(fileDir, 'backend'))

import json
from tools.leArquivos import leXls_Xlsx
from tools.funcoesUteis import removerAcentosECaracteresEspeciais, transformaCampoDataParaFormatoBrasileiro, retornaCampoComoData

wayToSaveFiles = open(os.path.join(fileDir, 'backend/extract/src/WayToSaveFiles.json') )
wayDefault = json.load(wayToSaveFiles)
wayToSaveFiles.close()

class AnalisaNotasImobilizado(object):
    def __init__(self):
        self._wayCompanies = os.path.join(wayDefault['wayDefaultToSaveFiles'], 'empresas.json')
        self._namesProductsBase =  leXls_Xlsx(os.path.join(wayDefault['wayDefaultToSaveFiles'], 'produtos_comparar.xlsx'))

        with open(self._wayCompanies) as companies:
            self._companies = json.load(companies)

        self._exportNotas = os.path.join(wayDefault['wayDefaultToSaveFiles'], 'analise_imobilizado.csv')
        self._exportNotas = open(self._exportNotas, 'w', encoding='utf-8')

        self._exportNotas.write(
            f"Codigo Empresa;Nome Empresa;CNPJ;Codigo Nota;Numero Nota;Codigo Fornecedor;Nome Fornecedor;Emissao;Entrada"
            f"Especie;Serie;Acumulador;Valor Contabil;Codigo Produto;Descricao;CFOP;Quantidade;Valor Unitario;Valor Total;Base ICMS;"
            f"Aliquota ICMS;Valor ICMS;Base ICMS ST;Valor ICMS ST\n"
        )
             
    def returnDataEmp(self, codi_emp):
        for companie in self._companies:
            if companie['codi_emp'] == codi_emp:
                return {
                    'name_emp': companie['nome_emp'], 'cnpj_emp': companie['cgce_emp']
                }

    def returnDataNote(self, wayNotes, codi_emp, codi_ent):
         with open(wayNotes) as notes:
            self._notes = json.load(notes)
            for note in self._notes:
                if note['codi_emp'] == codi_emp and note['codi_ent'] == codi_ent:
                    return note
    
    def noteIsAnAsset(self, notesProducts, notes):
        with open(notesProducts) as products:
            data = json.load(products)
            for product in data:
                if str(product['cfop_mep']) in ('1556', '2556', '1407', '2407'):
                    for nameProduct in self._namesProductsBase:
                        nameProduct = removerAcentosECaracteresEspeciais(nameProduct[0]).upper()

                        nameProductSystem = removerAcentosECaracteresEspeciais(product['desc_pdi']).upper()
                        if nameProductSystem.find(nameProduct) > 0:

                            dataEmp = self.returnDataEmp(product['codi_emp'])
                            dataNote = self.returnDataNote(notes, product['codi_emp'], product['codi_ent'])

                            dateEntrada = transformaCampoDataParaFormatoBrasileiro(retornaCampoComoData(dataNote['dent_ent'], 2))
                            dateEmissao = transformaCampoDataParaFormatoBrasileiro(retornaCampoComoData(dataNote['ddoc_ent'], 2))

                            print(f"- Processando empresa {product['codi_emp']} - {dataEmp['name_emp']}")

                            self._exportNotas.write(
                                f"{product['codi_emp']};"
                                f"{dataEmp['name_emp']};"
                                f"'{dataEmp['cnpj_emp']};"
                                f"{dataNote['codi_ent']};"
                                f"{dataNote['nume_ent']};"
                                f"{dataNote['codi_for']};"
                                f"{dataNote['nome_for']};"
                                f"{dateEmissao};"
                                f"{dateEntrada};"
                                f"{dataNote['codi_esp']};"
                                f"{dataNote['seri_ent']};"
                                f"{dataNote['codi_acu']};"
                                f"{dataNote['vcon_ent']};"
                                f"{str(product['codi_pdi']).strip()};"
                                f"{product['desc_pdi']};"
                                f"{product['cfop_mep']};"
                                f"{product['qtde_mep']};"
                                f"{product['valor_unit_mep']};"
                                f"{product['vlor_mep']};"
                                f"{product['bicms_mep']};"
                                f"{product['aliicms_mep']};"
                                f"{product['valor_icms_mep']};"
                                f"{product['bicmsst_mep']};"
                                f"{product['valor_subtri_mep']};"
                                f"\n"
                            )
      
    def processIfNoteIsAnAsset(self, filterCompanie=0):
        for companie in self._companies:
            if companie['stat_emp'] not in ('I') and companie['dina_emp'] is None:
                if companie['codi_emp'] == filterCompanie or filterCompanie == 0:
                    try:
                        self._wayEntryNotesProducts = os.path.join(wayDefault['wayDefaultToSaveFiles'], f"entradas_produtos/{companie['codi_emp']}-efmvepro.json")
                        self._wayEntryNotes = os.path.join(wayDefault['wayDefaultToSaveFiles'], f"entradas/{companie['codi_emp']}-efentradas.json")
                        self.noteIsAnAsset(self._wayEntryNotesProducts, self._wayEntryNotes)
                    except Exception as e:
                        print(e)
                            
