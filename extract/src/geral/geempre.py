import pandas as pd
import pyodbc
from db.ConexaoBanco import DB

class extractGeempre():
    def __init__(self):
        self._DB = DB()
        self._connection = self._DB.getConnection()
        self._cursor = None
        self._caminhoSalvarCSV = 'D:\\baymax\\arquivos\\extract\\geempre.csv'
        self._dataTotal = []
        self._data = []
        self._columns = []
        self._dataExport = {}

    def exportaDados(self):
        try:
            self._cursor = self._connection.cursor()
            sql = ("SELECT * FROM bethadba.geempre ORDER BY codi_emp")
            self._cursor.execute(sql)

            row = self._cursor.fetchone()
            for t in row.cursor_description:
                self._columns.append(t[0])

            # rows = self._cursor.fetchall()
            # for row in rows:
            #     for field in enumerate(row):
            #         field = str(field)
            #         field = field.replace('\n', '').replace('\r', '')
            #         self._data.append(field)
            #     self._dataTotal.append(self._data[:])
            #     self._data.clear()

            # for data in self._dataTotal:
            #     for fieldData in range(0, len(data)):
            #         self._dataExport[self._columns[fieldData]] = data[fieldData]
            
            # print(self._dataExport)

            # df = pd.DataFrame(self._dataTotal, self._columns)
            # print(df)

            df = pd.read_sql_query(sql, self._connection)

            print(df['cnae_emp'].dtype)
            df['cnae_emp'] = df['cnae_emp'].astype('float64')
            print(df['cnae_emp'])

            for column in self._columns:
                if df[column].dtype == 'int64':
                    df[column] = df[column].astype('int64')
                elif df[column].dtype == 'float64':
                    df[column] = df[column].astype('float64')
                else:
                    df[column] = df[column].astype(str).str.replace('\\r\\n', '')
                    df[column] = df[column].replace('\\n', '').replace('\\r', '').replace('\\t', '')

            df.to_csv(self._caminhoSalvarCSV, header=True, sep='|',float_format='%g',decimal='.', encoding='Windows-1252', na_rep='(null)', index=None)
        except Exception as e:
            print(f"Erro ao executar a consulta. O erro é: {e}")
        finally:
            if self._cursor is not None:
                self._cursor.close()
            self._DB.closeConnection()


