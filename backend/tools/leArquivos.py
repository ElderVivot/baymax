# -*- coding: utf-8 -*-

import xlrd
import os
import unicodedata
import re
import csv
import time
import sys
import datetime
import platform
import pytesseract as ocr
import json
from PIL import Image

fileDir = os.path.dirname(__file__)
sys.path.append(fileDir)

import funcoesUteis

def buscaArquivosEmPasta(caminho, extensao, buscarSubpastas=True):
    
    pastas = []
    lista_arquivos = []

    if buscarSubpastas == True:
        pastas = buscaSubpastas(caminho)
    else:
        pastas.append(caminho)

    for pasta in pastas:
        arquivos = os.listdir(pasta)
        
        for arquivo in arquivos:
            arquivo = str(arquivo).upper()
            if arquivo.endswith(extensao) and os.path.isdir(os.path.join(pasta,arquivo)) == False:
                lista_arquivos.append(os.path.join(pasta,arquivo))

    return lista_arquivos

def buscaSubpastas(caminhoPrincipal):

    subpastas = []

    def lePastas(caminho=caminhoPrincipal):

        pastas = os.listdir(caminho)
        if os.path.isdir(caminho):
            items = os.listdir(caminho)
            for item in items:
                novo_item = os.path.join(caminho,item)
                if os.path.isdir(novo_item):
                    subpastas.append(novo_item)
                    continue

    # chama sub função de ler as pastas
    lePastas()        
    
    # busca subpastas novamente
    for subpasta in subpastas:
        lePastas(caminho=subpasta)

    return subpastas

def leXls_Xlsx(arquivo):
    lista_dados = []
    dados_linha = []

    if os.path.getsize(arquivo) > 0:
        try:
            arquivo = xlrd.open_workbook(arquivo, logfile=open(os.devnull, 'w'))
        except Exception:
            arquivo = xlrd.open_workbook(arquivo, logfile=open(os.devnull, 'w'), encoding_override='Windows-1252')

        # guarda todas as planilhas que tem dentro do arquivo excel
        planilhas = arquivo.sheet_names()

        # lê cada planilha
        for p in planilhas:

            # pega o nome da planilha
            planilha = arquivo.sheet_by_name(p)

            # pega a quantidade de linha que a planilha tem
            max_row = planilha.nrows
            # pega a quantidade de colunca que a planilha tem
            max_column = planilha.ncols

            # lê cada linha e coluna da planilha e imprime
            for i in range(0, max_row):

                valor_linha = planilha.row_values(rowx=i)

                # ignora linhas em branco
                if valor_linha.count("") == max_column:
                    continue

                # lê as colunas
                for j in range(0, max_column):

                    # as linhas abaixo analisa o tipo de dado que está na planilha e retorna no formato correto, sem ".0" para números ou a data no formato numérico
                    tipo_valor = planilha.cell_type(rowx=i, colx=j)
                    valor_celula = funcoesUteis.removerAcentosECaracteresEspeciais(str(planilha.cell_value(rowx=i, colx=j)))
                    if tipo_valor == 2:
                        valor_casas_decimais = valor_celula.split('.')
                        valor_casas_decimais = valor_casas_decimais[1]
                        if int(valor_casas_decimais) == 0:
                            valor_celula = valor_celula.split('.')
                            valor_celula = valor_celula[0]
                    elif tipo_valor == 3:
                        valor_celula = float(planilha.cell_value(rowx=i, colx=j))
                        valor_celula = xlrd.xldate.xldate_as_datetime(valor_celula, datemode=0)
                        valor_celula = valor_celula.strftime("%d/%m/%Y")

                    # retira espaços e quebra de linha da célula
                    valor_celula = str(valor_celula).strip().replace('\n', '')

                    # adiciona o valor da célula na lista de dados_linha
                    dados_linha.append(valor_celula)

                # copia os dados da linha para o vetor de lista_dados
                lista_dados.append(dados_linha[:])

                # limpa os dados da linha para ler a próxima
                dados_linha.clear()

    # retorna uma lista dos dados
    return lista_dados

# def leCsv(arquivos=buscaArquivosEmPasta(extensao=(".csv")),saida="",separadorCampos=';'):
#     saida = open(saida, "w", encoding='utf-8')
#     lista_dados = []
#     dados_linha = []
#     for arquivo in arquivos:
#         with open(arquivo, 'rt') as csvfile:
#             csvreader = csv.reader(csvfile, delimiter=separadorCampos)
#             for row in csvreader:
#                 for campo in row:
#                     valor_celula = funcoesUteis.removerAcentosECaracteresEspeciais(str(campo))
                    
#                     # retira espaços e quebra de linha da célula
#                     valor_celula = str(valor_celula).strip().replace('\n', '')

#                     # gera o resultado num arquivo
#                     resultado = valor_celula + ';'
#                     resultado = resultado.replace('None', '')
#                     saida.write(resultado)

#                     # adiciona o valor da célula na lista de dados_linha
#                     dados_linha.append(valor_celula)

#                 # faz uma quebra de linha para passar pra nova linha
#                 saida.write('\n')

#                 # copia os dados da linha para o vetor de lista_dados
#                 lista_dados.append(dados_linha[:])

#                 # limpa os dados da linha para ler a próxima
#                 dados_linha.clear()

#     # fecha o arquivo
#     saida.close()

#     # retorna uma lista dos dados
#     return lista_dados

def ImageToText(arquivo):
    nome_arquivo = os.path.basename(arquivo)
    saida = f"temp\\" + str(nome_arquivo[0:len(nome_arquivo)-4]) + ".tmp"
    saida = open(saida, "w", encoding='utf-8')
    phrase = ocr.image_to_string(Image.open(arquivo), lang='por')
    saida.write(phrase)
    saida.close()

def PDFImgToText(arquivo):
    nome_arquivo = os.path.basename(arquivo)
    saida = f"temp\\" + str(nome_arquivo[0:len(nome_arquivo)-4]) + ".jpg"

    comando = f"magick -density 300 \"{arquivo}\" \"{saida}\""
    os.system(comando)

    ImageToText(saida)
    
def PDFToText(arquivo, mode = "simple"):
    nome_arquivo = os.path.basename(arquivo)
    saida = f"temp\\" + str(nome_arquivo[0:len(nome_arquivo)-4]) + ".tmp"
    try:
        # verifica se o Windows é 32 ou 64 bits
        architecture = platform.architecture()
        if architecture[0].count('32') > 0:
            pdftotext = "pdftotext32.exe"
        else:
            pdftotext = "pdftotext64.exe"
        
        # chama o comando pra transformação do PDF
        comando = f"exe\\{pdftotext} -{mode} \"{arquivo}\" \"{saida}\""
        os.system(comando)

        # analisa se o PDF é uma imagem
        tamanho_arquivo = os.path.getsize(saida)
        if(tamanho_arquivo <= 5):
            PDFImgToText(arquivo)

    except Exception as ex:
        print(f"Nao foi possivel transformar o arquivo \"{arquivo}\". O erro é: {str(ex)}")

def leTxt(caminho, encoding='utf-8', treatAsText=False, removeBlankLines=False):
    lista_linha = []
    
    # le o arquivo e grava num vetor
    try:
        with open(caminho, 'rt', encoding=encoding) as txtfile:
            for linha in txtfile:
                linha = str(linha).replace("\n", "")
                if treatAsText is True:
                    linha = funcoesUteis.treatTextField(linha)
                if removeBlankLines is True:
                    if linha.strip() == "":
                        continue
                lista_linha.append(linha)
        txtfile.close()
    except Exception as e:
        with open(caminho, 'rt', encoding='Windows-1252') as txtfile:
            for linha in txtfile:
                linha = str(linha).replace("\n", "")
                if treatAsText is True:
                    linha = funcoesUteis.treatTextField(linha)
                if removeBlankLines is True:
                    if linha.strip() == "":
                        continue
                lista_linha.append(linha)
        txtfile.close()

    return lista_linha

def readJson(caminho):
    try:
        with open(caminho) as file:
            return json.load(file)
    except Exception as e:
        print(e)
