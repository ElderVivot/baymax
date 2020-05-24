import os
import sys
import unicodedata
import re
import datetime
import hashlib
import json
import shutil
from validate_docbr import CNPJ, CPF

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(fileDir)
sys.path.append(os.path.join(fileDir, 'backend'))
sys.path.append(os.path.dirname(__file__))

import leArquivos

def removerAcentosECaracteresEspeciais(palavra):
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra).encode('ASCII', 'ignore').decode('ASCII')
    palavraTratada = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com valores corretos
    return re.sub('[^a-zA-Z0-9.!+:>=)?$(/*,\-_ \\\]', '', palavraTratada)

def trocaCaracteresTextoPraLetraX(palavra):
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra).encode('ASCII', 'ignore').decode('ASCII')
    palavraTratada = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com valores corretos
    return re.sub('[^0-9\\-/]', 'X', palavraTratada)

def justLettersNumbersDots(palavra):
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra).encode('ASCII', 'ignore').decode('ASCII')
    palavraTratada = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com valores corretos
    return re.sub('[^a-zA-Z0-9.!+:>=)?(/*,\-_ \\\]', '', palavraTratada)

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

def analyzeIfFieldIsValid(data, name, returnDefault="", otherComparationName=""):
    try:
        if otherComparationName == "":
            return data[name]
        else:
            return data[name, otherComparationName]
    except Exception:
        return returnDefault

def returnDataFieldInDict(data, valuesList, valueDefault=''):
    lenList = len(valuesList)

    try:
        if lenList == 1:
            return data[valuesList[0]]
        elif lenList == 2:
            return data[valuesList[0]][valuesList[1]]
        elif lenList == 3:
            return data[valuesList[0]][valuesList[1]][valuesList[2]]
        elif lenList == 4:
            return data[valuesList[0]][valuesList[1]][valuesList[2]][valuesList[3]]
        elif lenList == 5:
            return data[valuesList[0]][valuesList[1]][valuesList[2]][valuesList[3]][valuesList[4]]
        elif lenList == 6:
            return data[valuesList[0]][valuesList[1]][valuesList[2]][valuesList[3]][valuesList[4]][valuesList[5]]
        else:
            return ""
    except Exception:
        return valueDefault


def analyzeIfFieldIsValidMatrix(data, position, returnDefault="", positionOriginal=False):
    # :data é o vetor com as informações
    # :position a posição que a informação que quero retornar se encontra no vetor
    # :returnDefault caso não encontre a posição qual valor deve retornar
    # :positionOriginal é pra não subtrair por menos 1 o retorno, por padrão eu passo o número normal e ele subtrai um visto que o vetor
    # começa com zero. Quando True ele não faz esta substração.
    try:
        if positionOriginal is False:
            return data[position-1]
        else:
            return data[position]
    except Exception:
        return returnDefault

def analyzeIfFieldHasPositionInFileEnd(data, positionInFile, positionInFileEnd):
    positionInFile = positionInFile-1
    
    try:
        if positionInFileEnd <= 0:
            return data[positionInFile]
        else:
            return ''.join(data[positionInFile:positionInFileEnd])
    except Exception:
        return ""

def treatTextField(value):
    try:
        return minimalizeSpaces(removerAcentosECaracteresEspeciais(value.strip().upper()))
    except Exception:
        return ""

def treatTextFieldInVector(data, numberOfField=0, fieldsHeader=[], nameFieldHeader='', positionInFileEnd=0):
    """
    :param data: Informar o array de dados que quer ler
    :param numberOfField: numero do campo na planilha (opcional)
    :param fieldsHeader: linha do cabeçalho armazenado num vetor (opcional)
    :param nameFieldHeader: nome do cabeçalho que é pra buscar (opcional)
    :return: retorna um campo como texto, retirando acentos, espaços excessivos, etc
    """
    if len(fieldsHeader) > 0 and nameFieldHeader is not None and nameFieldHeader != "":
        try:
            return treatTextField(data[searchPositionFieldForName(fieldsHeader, nameFieldHeader)])
        except Exception:
            try:
                return treatTextField(analyzeIfFieldHasPositionInFileEnd(data, numberOfField, positionInFileEnd))
            except Exception:
                return ""
    else:
        try:
            return treatTextField(analyzeIfFieldHasPositionInFileEnd(data, numberOfField, positionInFileEnd))
        except Exception:
            return ""

def treatTextFieldInDictionary(data, nameField):
    """
    :param data: Informar o dicionário de dados que quer ler
    :param nameField: nome do campo a ser lido
    """
    try:
        return treatTextField(data[nameField])
    except Exception:
        return ""            

def treatNumberField(value, isInt=False):
    if type(value) == int:
        return value
    try:
        value = re.sub("[^0-9]", '', value)
        if value == "":
            return 0
        else:
            if isInt is True:
                try:
                    return int(value)
                except Exception as e:
                    return 0
            return value
    except Exception:
        return 0

def treatNumberFieldInVector(data, numberOfField=-1, fieldsHeader=[], nameFieldHeader='', isInt=False, positionInFileEnd=0):
    """
    :param data: Informar o array de dados que quer ler
    :param numberOfField: numero do campo na planilha (opcional)
    :param fieldsHeader: linha do cabeçalho armazenado num vetor (opcional)
    :param nameFieldHeader: nome do cabeçalho que é pra buscar (opcional)
    :return: retorna um campo apenas como número
    """
    if len(fieldsHeader) > 0 and nameFieldHeader is not None and nameFieldHeader != "":
        try:
            return treatNumberField(data[searchPositionFieldForName(fieldsHeader, nameFieldHeader)], isInt)
        except Exception:
            try:
                return treatNumberField(analyzeIfFieldHasPositionInFileEnd(data, numberOfField, positionInFileEnd), isInt)
            except Exception:
                return 0
    else:
        try:
            return treatNumberField(analyzeIfFieldHasPositionInFileEnd(data, numberOfField, positionInFileEnd), isInt)
        except Exception:
            return 0 

def treatNumberFieldInDictionary(data, nameField, isInt=False):
    """
    :param data: Informar o dicionário de dados que quer ler
    :param nameField: nome do campo a ser lido
    """
    try:
        return treatNumberField(data[nameField], isInt)
    except Exception:
        return 0

def treatDecimalField(value, numberOfDecimalPlaces=2):
    if type(value) == float:
        return value
    try:
        value = str(value)
        value = re.sub('[^0-9.,-]', '', value)
        if value.find(',') >= 0 and value.find('.') >= 0:
            value = value.replace('.','')

        if value.find(',') >= 0:
            value = value.replace(',','.')

        if value.find('.') < 0:
            value = int(value)
        
        return float(value)
    except Exception as e:
        return float(0)

def treatDecimalFieldInVector(data, numberOfField=0, fieldsHeader=[], nameFieldHeader='', row='main', positionInFileEnd=0):
    """
    :param data: Informar o array de dados que quer ler
    :param numberOfField: numero do campo na planilha (opcional)
    :param fieldsHeader: linha do cabeçalho armazenado num vetor (opcional)
    :param nameFieldHeader: nome do cabeçalho que é pra buscar (opcional)
    :param row: este serve pra caso não seja um pagamento que esteja na linha principal (que não tem cabeçalho, então pegar apenas pelo número do campo). O valor 'main' quer dizer que tá numa linha que pode ter cabeçalho
    :return: retorna um campo como decimal
    """
    if len(fieldsHeader) > 0 and nameFieldHeader is not None and nameFieldHeader != "":
        try:
            if row == 'main':
                return treatDecimalField(data[searchPositionFieldForName(fieldsHeader, nameFieldHeader)])
            else:
                return treatDecimalField(analyzeIfFieldHasPositionInFileEnd(data, numberOfField, positionInFileEnd))
        except Exception:
            try:
                return treatDecimalField(analyzeIfFieldHasPositionInFileEnd(data, numberOfField, positionInFileEnd))
            except Exception:
                return float(0)
    else:
        try:
            return treatDecimalField(analyzeIfFieldHasPositionInFileEnd(data, numberOfField, positionInFileEnd))
        except Exception:
            return float(0)

def retornaCampoComoData(valorCampo, formatoData=1):
    """
    :param valorCampo: Informar o campo string que será transformado para DATA
    :param formatoData: 1 = 'DD/MM/YYYY' ; 2 = 'YYYY-MM-DD' ; 3 = 'YYYY/MM/DD' ; 4 = 'DDMMYYYY'
    :return: retorna como uma data. Caso não seja uma data válida irá retornar None
    """
    if type(valorCampo) == 'datetime.date':
        return valorCampo

    valorCampo = str(valorCampo).strip()

    lengthField = 10 # tamanho padrão da data são 10 caracteres, só muda se não tiver os separados de dia, mês e ano

    if formatoData == 1:
        formatoDataStr = "%d/%m/%Y"
    elif formatoData == 2:
        formatoDataStr = "%Y-%m-%d"
    elif formatoData == 3:
        formatoDataStr = "%Y/%m/%d"
    elif formatoData == 4:
        formatoDataStr = "%d%m%Y"
        lengthField = 8

    try:
        return datetime.datetime.strptime(valorCampo[:lengthField], formatoDataStr).date()
    except ValueError:
        return None

def treatDateFieldInVector(data, numberOfField=0, fieldsHeader=[], nameFieldHeader='', formatoData=1, row='main', positionInFileEnd=0):
    """
    :param data: Informar o array de dados que quer ler
    :param numberOfField: numero do campo na planilha (opcional)
    :param fieldsHeader: linha do cabeçalho armazenado num vetor (opcional)
    :param nameFieldHeader: nome do cabeçalho que é pra buscar (opcional)
    :param formatoData: 1 = 'DD/MM/YYYY' ; 2 = 'YYYY-MM-DD (opcional)
    :param row: este serve pra caso não seja um pagamento que esteja na linha principal (que não tem cabeçalho, então pegar apenas pelo número do campo). O valor 'main' quer dizer que tá numa linha que pode ter cabeçalho
    :return: retorna um campo como decimal
    """
    if len(fieldsHeader) > 0 and nameFieldHeader is not None and nameFieldHeader != "":
        try:
            if row == 'main':
                return retornaCampoComoData(data[searchPositionFieldForName(fieldsHeader, nameFieldHeader)], formatoData)
            else:
                return retornaCampoComoData(analyzeIfFieldHasPositionInFileEnd(data, numberOfField, positionInFileEnd), formatoData)
        except Exception:
            try:
                return retornaCampoComoData(analyzeIfFieldHasPositionInFileEnd(data, numberOfField, positionInFileEnd), formatoData)
            except Exception:
                return None
    else:
        try:
            return retornaCampoComoData(analyzeIfFieldHasPositionInFileEnd(data, numberOfField, positionInFileEnd), formatoData)
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

def transformDateFieldToString(valueField, formatDate=2):
    """
    :param valueField: informe o campo como 'data'
    :param formatDate: o 1 é pra retornar no formato brasileiro, o 2 no formato amaricano
    :return: traz a data no formato brasileiro (dd/mm/yyyy) ou americano (yyyy-mm-dd)
    """
    try:
        if formatDate == 1:
            return valueField.strftime("%d/%m/%Y")
        else:
            return valueField.strftime("%Y-%m-%d")
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
    try:
        for array in arraySet:
            if array is None:
                continue
            for vector in array:
                if len(vector) == 0:
                    continue
                newArray.append(vector)
    except Exception:
        pass
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
    return dateTimeObj.strftime("%Y_%m_%d_%H_%M")

def returnBankForName(nameBank):
    nameBank = str(nameBank)
    if nameBank.count('BRASIL') > 0:
        nameBank = 'BRASIL'
    elif nameBank.count('BRADESCO') > 0:
        nameBank = 'BRADESCO'
    elif ( nameBank.count('CAIXA') > 0 and ( nameBank.count('ECON') > 0 or nameBank.count('AG.') > 0 or nameBank.count('FEDERAL') > 0 ) ) or nameBank.count('CEF') > 0:
        nameBank = 'CEF'
    elif nameBank.count('SICOOB') > 0:
        nameBank = 'SICOOB'
    elif nameBank.count('SICRED') > 0:
        nameBank = 'SICRED'
    elif nameBank.count('SANTANDER') > 0:
        nameBank = 'SANTANDER'
    elif nameBank.count('ITAU') > 0:
        nameBank = 'ITAU'
    elif nameBank.count('SAFRA') > 0:
        nameBank = 'SAFRA'
    elif nameBank.count('DINHEIRO') > 0:
        nameBank = 'DINHEIRO'
    else:
        nameBank = nameBank

    return nameBank

def returnBankForNumber(numberBank):
    numberBankOriginal = numberBank
    numberBank = treatNumberField(numberBank, True)
    nameBank = ""
    if numberBank == 1:
        nameBank = 'BRASIL'
    elif numberBank == 3:
        nameBank = 'AMAZONIA'
    elif numberBank == 237:
        nameBank = 'BRADESCO'
    elif numberBank == 104:
        nameBank = 'CEF'
    elif numberBank == 756:
        nameBank = 'SICOOB'
    elif numberBank == 748:
        nameBank = 'SICRED'
    elif numberBank == 33:
        nameBank = 'SANTANDER'
    elif numberBank == 341:
        nameBank = 'ITAU'
    elif numberBank == 743:
        nameBank = 'SEMEAR'
    elif numberBank == 422:
        nameBank = 'SAFRA'
    elif numberBank == 637:
        nameBank = 'SOFISA'
    else:
        nameBank = numberBankOriginal

    return nameBank

def updateFilesRead(wayTempFileRead, file, layoutModel):
    filesRead = leArquivos.readJson(wayTempFileRead)

    filesWrite = open(wayTempFileRead, 'w')

    wayFile = file.replace('/', '\\')
    filesRead[wayFile] = layoutModel

    json.dump(filesRead, filesWrite)

    filesWrite.close()

def handleNote(nota, lista_char=["-","/"]):
    for char in lista_char:
        if nota.count(char) > 0:
            nota = nota.split(char)
            nota = nota[0]
            break
    return treatNumberField(nota)

def validateCPF(value):
    cpf = CPF()
    return cpf.validate(value)

def validateCNPJ(value):
    cnpj = CNPJ()
    return cnpj.validate(value)