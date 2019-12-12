import os
import sys

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(fileDir)

import unicodedata
import re
import datetime
import hashlib
import json

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

def searchPositionFieldForName(header, nameField=''):
    nameField = treatTextField(nameField)
    try:
        positionOfField = header[nameField]
    except Exception:
        positionOfField = -1

    return positionOfField

def analyzeIfFieldIsValid(data, name, returnDefault=""):
    try:
        return data[name]
    except Exception:
        return returnDefault

def treatTextField(value):
    try:
        return minimalizeSpaces(removerAcentosECaracteresEspeciais(value.strip().upper()))
    except Exception:
        return ""

def treatTextFieldInVector(data, numberOfField=0, fieldsHeader=[], nameFieldHeader=''):
    """
    :param data: Informar o array de dados que quer ler
    :param numberOfField: numero do campo na planilha (opcional)
    :param fieldsHeader: linha do cabeçalho armazenado num vetor (opcional)
    :param nameFieldHeader: nome do cabeçalho que é pra buscar (opcional)
    :return: retorna um campo como texto, retirando acentos, espaços excessivos, etc
    """
    if numberOfField > 0:
        try:
            return treatTextField(data[numberOfField-1])
        except Exception:
            return ""
    else:
        try:
            return treatTextField(data[searchPositionFieldForName(fieldsHeader, nameFieldHeader)])
        except Exception:
            return ""

def treatNumberField(value):
    try:
        return re.sub("[^0-9]", '', value)
    except Exception:
        return 0

def treatNumberFieldInVector(data, numberOfField=-1, fieldsHeader=[], nameFieldHeader=''):
    """
    :param data: Informar o array de dados que quer ler
    :param numberOfField: numero do campo na planilha (opcional)
    :param fieldsHeader: linha do cabeçalho armazenado num vetor (opcional)
    :param nameFieldHeader: nome do cabeçalho que é pra buscar (opcional)
    :return: retorna um campo apenas como número
    """
    if numberOfField >= 0:
        try:
            return treatNumberField(data[numberOfField-1])
        except Exception:
            return 0
    else:
        try:
            return treatNumberField(data[searchPositionFieldForName(fieldsHeader, nameFieldHeader)])
        except Exception:
            return 0

def treatDecimalField(value, numberOfDecimalPlaces=2):
    try:
        value = str(value)
        value = re.sub('[^0-9.,-]', '', value)
        if value.find(',') > 0 and value.find('.') > 0:
            value = value.replace('.','')

        if value.find(','):
            value = value.replace(',','.')
        
        return float(value)
    except Exception:
        return float(0)

def treatDecimalFieldInVector(data, numberOfField=0, fieldsHeader=[], nameFieldHeader=''):
    """
    :param data: Informar o array de dados que quer ler
    :param numberOfField: numero do campo na planilha (opcional)
    :param fieldsHeader: linha do cabeçalho armazenado num vetor (opcional)
    :param nameFieldHeader: nome do cabeçalho que é pra buscar (opcional)
    :return: retorna um campo como decimal
    """
    if numberOfField > 0:
        try:
            return treatDecimalField(data[numberOfField-1])
        except Exception:
            return float(0)
    else:
        try:
            return treatDecimalField(data[searchPositionFieldForName(fieldsHeader, nameFieldHeader)])
        except Exception:
            return float(0)

def retornaCampoComoData(valorCampo, formatoData=1):
    """
    :param valorCampo: Informar o campo string que será transformado para DATA
    :param formatoData: 1 = 'DD/MM/YYYY' ; 2 = 'YYYY-MM-DD
    :return: retorna como uma data. Caso não seja uma data válida irá retornar None
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

def treatDateFieldInVector(data, numberOfField=0, fieldsHeader=[], nameFieldHeader='', formatoData=1):
    """
    :param data: Informar o array de dados que quer ler
    :param numberOfField: numero do campo na planilha (opcional)
    :param fieldsHeader: linha do cabeçalho armazenado num vetor (opcional)
    :param nameFieldHeader: nome do cabeçalho que é pra buscar (opcional)
    :param formatoData: 1 = 'DD/MM/YYYY' ; 2 = 'YYYY-MM-DD (opcional)
    :return: retorna um campo como decimal
    """
    if numberOfField > 0:
        try:
            return retornaCampoComoData(data[numberOfField-1], formatoData)
        except Exception:
            return None
    else:
        try:
            return retornaCampoComoData(data[searchPositionFieldForName(fieldsHeader, nameFieldHeader)], formatoData)
        except Exception:
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

def md5Checksum(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

def removeAnArrayFromWithinAnother(arraySet=[]):
    newArray = []
    for array in arraySet:
        for vector in array:
            if len(vector) == 0:
                continue
            newArray.append(vector)
    return newArray

def removeAnDictionaryFromWithinArray(arraySet=[]):
    newDictonary = {}
    for dictonary in arraySet:
        for key, value in dictonary.items():
            if value == "":
                continue
            newDictonary[key] = value
    return newDictonary

def getOnlyNameFile(nameFileOriginal):
    nameFileSplit = nameFileOriginal.split('.')
    nameFile = '.'.join(nameFileSplit[:-1])
    return nameFile

def getDateTimeNowInFormatStr():
    dateTimeObj = datetime.datetime.now()
    return dateTimeObj.strftime("%Y_%m_%d %H_%M_%S")