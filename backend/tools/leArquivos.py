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
import PyPDF2
import warnings
import slate3k as slate
import logging
from PIL import Image
import xmltodict as xmldict

# pra ignorar erros que dá no momento de ler um PDF por exemplo
warnings.filterwarnings("ignore")
logging.propagate = False 
logging.getLogger().setLevel(logging.ERROR)

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

def leXls_Xlsx(arquivo, nameSheetToFilter='filterAll'):
    lista_dados = []
    dados_linha = []

    if os.path.getsize(arquivo) > 0:
        try:
            arquivo = xlrd.open_workbook(arquivo, logfile=open(os.devnull, 'w'))
        except Exception:
            try:
                arquivo = xlrd.open_workbook(arquivo, logfile=open(os.devnull, 'w'), encoding_override='Windows-1252')
            except Exception:
                return []

        # guarda todas as planilhas que tem dentro do arquivo excel
        planilhas = arquivo.sheet_names()

        # lê cada planilha
        for sheetName in planilhas:

            # pega os dados da planilha
            planilha = arquivo.sheet_by_name(sheetName)

            # continue only if name sheet equal the name filter of argument
            if funcoesUteis.treatTextField(sheetName) == funcoesUteis.treatTextField(nameSheetToFilter) or nameSheetToFilter == 'filterAll':
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
                            try:
                                if int(valor_casas_decimais) == 0:
                                    valor_celula = valor_celula.split('.')
                                    valor_celula = valor_celula[0]
                            except Exception:
                                valor_celula = valor_celula
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
            else:
                continue
    # retorna uma lista dos dados
    return lista_dados

def readCsv(arquivo,separadorCampos=';'):
    lista_dados = []
    dados_linha = []
    
    nome_arquivo = os.path.basename(arquivo)

    with open(arquivo, 'rt') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=separadorCampos)
        for row in csvreader:
            
            existe_valor_linha = ""
            for campo in row:
                valor_celula = funcoesUteis.treatTextField(campo)
                existe_valor_linha += valor_celula
            
            # se não existir nenhum valor na linha passa pra próxima
            if existe_valor_linha == "":
                continue

            for campo in row:
                valor_celula = funcoesUteis.treatTextField(campo)

                # adiciona o valor da célula na lista de dados_linha
                dados_linha.append(valor_celula)

            # copia os dados da linha para o vetor de lista_dados
            lista_dados.append(dados_linha[:])

            # limpa os dados da linha para ler a próxima
            dados_linha.clear()

    # retorna uma lista dos dados
    return lista_dados

def ImageToText(file, wayToSaveFile):
    nameFile = funcoesUteis.getOnlyNameFile(os.path.basename(file))
    wayToSave = f"{wayToSaveFile}/{nameFile}.txt"
    wayToSave = open(wayToSave, "w", encoding='utf-8')
    content = ocr.image_to_string(Image.open(file), lang='por')
    wayToSave.write(content)
    wayToSave.close()

def PDFImgToText(file, wayToSaveFile):
    nameFile = funcoesUteis.getOnlyNameFile(os.path.basename(file))
    wayToSave = f"{wayToSaveFile}/{nameFile}.jpg"

    command = f'magick -density 300 "{file}" "{wayToSave}"'
    os.system(command)

    ImageToText(wayToSave, wayToSaveFile)
    
def PDFToText(file, wayToSaveFile, mode="simple"):
    nameFile = funcoesUteis.getOnlyNameFile(os.path.basename(file))
    wayToSave = f"{wayToSaveFile}/{nameFile}.txt"
    try:
        textPdf = ""
        with open(file, 'rb') as filePdf:
            documents = slate.PDF(filePdf)
            for document in documents:
                textPdf += document
            
        if funcoesUteis.treatTextField(textPdf) == "":
            PDFImgToText(file, wayToSaveFile)
        else:
            command = f'{fileDir}/exe/pdftotext64.exe -{mode} "{file}" "{wayToSave}"'
            os.system(command)

    except Exception as ex:
        print(f"Nao foi possivel transformar o arquivo \"{file}\". O erro é: {str(ex)}")

# PDFToText('C:/Programming/baymax/backend/accounting_integration/data/temp/1428/pdfs/01-10-19 placo 20747-005 - diviart/1.pdf', 'C:/Programming/baymax/backend/accounting_integration/data/temp/1428/pdfs/01-10-19 placo 20747-005 - diviart')

def splitPdfOnePageEach(file, wayToSaveFiles, sequential=0):
    try:
        nameFile = funcoesUteis.getOnlyNameFile(os.path.basename(file))

        nameDirectoryToSave = f"{nameFile}-{sequential}"

        wayBaseToSaveFile = os.path.join(wayToSaveFiles, 'pdfs', nameDirectoryToSave)
        os.makedirs(wayBaseToSaveFile)

        with open(file, 'rb') as filePdf:
            pdfReader = PyPDF2.PdfFileReader(filePdf)
            countPages = pdfReader.getNumPages()

            for numberPage in range(countPages):
                pageContent = pdfReader.getPage(numberPage)
                
                pdfWriter = PyPDF2.PdfFileWriter()
                pdfWriter.addPage(pageContent)

                with open(f'{wayBaseToSaveFile}\\{numberPage+1}.pdf', 'wb') as newPdfPerPage:
                    pdfWriter.write(newPdfPerPage)
    except Exception as e:
        pass #print(f'\t - Não foi possível processar o arquivo {file}, provavelmente o PDF está inválido e com erro no momento de abrir!')

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

    return lista_linha

def readSql(wayFile, nameSql, *args):
    # esta função lê um SQL e retorna como string com os *args aplicados. Pro arg ser aplicado tem que colocar um '#' no lugar, 
    # que ele deve fazer a substituição
    sql = ''
    argSequencial = 0
    try:
        with open(os.path.join(wayFile, nameSql), 'rt') as sqlfile:
            for row in sqlfile:
                positionInicialSearchNewHashtag = 0
                rowWithArguments = ''
                positionFindHashtag = row.find('#')
                rowSplit = row
                if positionFindHashtag >= 0:
                    while True:
                        rowWithArguments += f'{rowSplit[:positionFindHashtag]}{args[argSequencial]}'
                        positionInicialSearchNewHashtag = positionFindHashtag+1
                        rowSplit = rowSplit[positionInicialSearchNewHashtag:]
                        positionFindHashtag = rowSplit.find('#')
                        if positionFindHashtag < 0:
                            rowWithArguments += rowSplit                            
                            argSequencial += 1
                            break
                        else:
                            argSequencial += 1
                
                row = rowWithArguments if rowWithArguments != "" else row
                sql += row
    except Exception:
        sql = ''
    
    return sql

def readJson(caminho):
    try:
        with open(caminho) as file:
            return json.load(file)
    except Exception as e:
        print(e)

def readXml(way):
    try:
        with open(way) as file:
            return xmldict.parse(file.read())
    except Exception as e:
        return {}
