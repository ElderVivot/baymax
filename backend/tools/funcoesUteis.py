import os
import sys

fileDir = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(fileDir)

import unicodedata
import re
import datetime
import hashlib

def removerAcentosECaracteresEspeciais(palavra):
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra).encode('ASCII', 'ignore').decode('ASCII')
    palavraTratada = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com valores corretos
    return re.sub('[^a-zA-Z0-9.!+:=)?$(/*,\-_ \\\]', '', palavraTratada)

def trocaCaracteresTextoPraLetraX(palavra):
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra).encode('ASCII', 'ignore').decode('ASCII')
    palavraTratada = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com valores corretos
    return re.sub('[^0-9\\-/]', 'X', palavraTratada)

# Minimaliza, ou seja, transforma todas as instancias repetidas de espaços em espaços simples.
#   Exemplo, o texto "  cnpj:      09.582.876/0001-68    Espécie Documento          Aceite" viraria
#   "cnpj: 09.582.876/0001-68 Espécie Documento Aceite"
#
# Nota: Ele faz um trim do texto também
def minimalizeSpaces(text):
    _result = text
    while ("  " in _result):
        _result = _result.replace("  ", " ")
    _result = _result.strip()
    return _result

def handlesTextField(value):
    try:
        return minimalizeSpaces(removerAcentosECaracteresEspeciais(value.strip().upper()))
    except Exception:
        return ""

def handlesTextFieldInVector(data, numberOfField=0, fieldsHeader=[], nameFieldHeader=''):
    if numberOfField > 0:
        try:
            return handlesTextField(data[numberOfField])
        except Exception:
            return ""
    # criar o else pra planilhas que tem o cabeçalho
    else:
        return ""

def handlesNumberField(value):
    try:
        return re.sub("[^0-9]", '', value)
    except Exception:
        return 0

def handlesNumberFieldInVector(data, numberOfField=-1, fieldsHeader=[], nameFieldHeader=''):
    if numberOfField >= 0:
        try:
            return handlesNumberField(data[numberOfField])
        except Exception:
            return 0
    # criar o else pra planilhas que tem o cabeçalho
    else:
        return 0

def handlesDecimalField(value, numberOfDecimalPlaces=2):
    try:
        value = str(value)
        value = re.sub('[^0-9.,]', '', value)
        if value.find(',') > 0 and value.find('.') > 0:
            value = value.replace('.','')

        if value.find(','):
            value = value.replace(',','.')
        
        return float(value)
    except Exception:
        return float(0)

def handlesDecimalFieldInVector(data, numberOfField=0, fieldsHeader=[], nameFieldHeader=''):
    if numberOfField > 0:
        try:
            return handlesDecimalField(data[numberOfField])
        except Exception:
            return float(0)
    # criar o else pra planilhas que tem o cabeçalho
    else:
        return float(0)

def retornaCampoComoData(valorCampo, formatoData=1):
    """
    :param valorCampo: Informar o campo string que será transformado para DATA
    :param formatoData: 1 = 'DD/MM/YYYY' ; 2 = 'YYYY-MM-DD; 3 = ISO'
    :return: retorna como uma data. Caso não seja uma data válida irá retornar um campo vazio
    """
    valorCampo = str(valorCampo).strip()

    if formatoData == 1:
        formatoDataStr = "%d/%m/%Y"
    elif formatoData == 2:
        formatoDataStr = "%Y-%m-%d"

    try:
        return datetime.datetime.strptime(valorCampo[:10], formatoDataStr).date()
    except ValueError:
        return None

def transformaCampoDataParaFormatoBrasileiro(valorCampo):
    """
    :param valorCampo: informe o campo data, deve buscar da função retornaCampoComoData()
    :return: traz a data no formato brasileiro (dd/mm/yyyy)
    """
    try:
        return valorCampo.strftime("%d/%m/%Y")
    except AttributeError:
        return None

def buscaPosicaoCampo(campoCabecalho, nomeCampo='', posicaoCampo=0):
    nomeCampo = str(removerAcentosECaracteresEspeciais(nomeCampo)).upper()
    try:
        numPosicaoCampo = campoCabecalho[nomeCampo]
    except KeyError:
        numPosicaoCampo = posicaoCampo

    return numPosicaoCampo

def md5Checksum(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()