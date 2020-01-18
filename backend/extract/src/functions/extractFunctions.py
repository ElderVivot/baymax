# coding: utf-8

import os
import sys

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend/extract/src'))
sys.path.append(os.path.join(fileDir, 'backend'))

import pandas as pd
import tools.funcoesUteis as funcoesUteis

def parseTypeFiedValueCorrect(df, columns):
    for column in columns:
        if df[column].dtype == 'int64':
            df[column] = df[column].astype('int64')
            # df[column] = df[column].astype(str)
        elif df[column].dtype == 'float64':
            df[column] = df[column].astype('float64')
            # df[column] = df[column].astype(str)
        else:
            df[column] = df[column].astype(str).str.replace('\\r\\n', '')
            df[column] = df[column].replace('\\n', '').replace('\\r', '').replace('\\t', '')

    return df

def returnCompetenceStartEnd(companie, filterMonthStart, filterYearStart, filterMonthEnd, filterYearEnd):
    dcad_emp = funcoesUteis.retornaCampoComoData(funcoesUteis.returnDataFieldInDict(companie, ['dcad_emp']), 2)
    dina_emp = funcoesUteis.retornaCampoComoData(funcoesUteis.returnDataFieldInDict(companie, ['dina_emp']), 2)

    if dcad_emp is not None:
        if dcad_emp.year > filterYearStart:
            filterYearStart = dcad_emp.year
            if dcad_emp.month > filterMonthStart:
                filterMonthStart = dcad_emp.month

    if dina_emp is not None:
        if dina_emp.year < filterYearEnd:
            filterYearEnd = dina_emp.year
            if dina_emp.month < filterMonthEnd:
                filterMonthEnd = dina_emp.month

    return {
        "filterMonthStart": filterMonthStart,
        "filterYearStart": filterYearStart,
        "filterMonthEnd": filterMonthEnd,
        "filterYearEnd": filterYearEnd
    }

def returnMonthsOfYear(year, filterMonthStart, filterYearStart, filterMonthEnd, filterYearEnd):
    if year == filterYearStart and year == filterMonthEnd:
        months = list(range(filterMonthStart, filterMonthEnd+1)) # o mais 1 é pq o range pega só pega do inicial até o último antes do final, exemplo: range(0,3) = [0,1,2]
    elif year == filterYearStart:
        months = list(range(filterMonthStart, 13))
    elif year == filterYearEnd:
        months = list(range(1, filterMonthEnd+1))
    else:
        months = list(range(1,13))

    return months

