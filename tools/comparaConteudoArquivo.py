# -*- coding: utf-8 -*-

import os
from os.path import dirname, join, abspath
import sys
sys.path.append(abspath(join(dirname(__file__), '..')))
import leArquivos
import operator

def analisaArquivo():

    pasta = input(str('- Informe o caminho da pasta: '))

    dadosArquivos = {}

    for raiz, diretorios, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            caminhoArquivo = os.path.join(raiz,arquivo)
            if arquivo.upper().endswith(('.XLS')):
                dadosArquivos[arquivo] = leArquivos.leXls_Xlsx(caminhoArquivo)
            else:
                continue

    ranking = []
    ranking = sorted(dadosArquivos.items(), key = operator.itemgetter(1), reverse=False)
    #print(ranking)

    for key, value in enumerate(ranking):
        #print(key, ranking[key+1][1])
        if key > 0:
            if ranking[key-1][1] == ranking[key][1]:
                print(f'- Os arquivos {ranking[key-1][0]} e {ranking[key][0]} possuem exatamente a mesma informação')

analisaArquivo()