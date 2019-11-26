import pandas as pd

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