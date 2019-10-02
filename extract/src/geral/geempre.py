import pandas as pd
import pyodbc
from db.ConexaoBanco import DB

class extractGeempre():
    def __init__(self):
        self._DB = DB()
        self._connection = self._DB.getConnection()
        self._cursor = None
        self._caminhoSalvarCSV = 'D:\\baymax\\arquivos\\extract\\geempre.csv'
        self._dataExport = []
        self._data = []

    def exportaDados(self):
        try:
            self._cursor = self._connection.cursor()
            sql = ("SELECT * FROM bethadba.geempre ORDER BY codi_emp")
            self._cursor.execute(sql)
            rows = self._cursor.fetchall()

            for row in rows:
                for field in row:
                    # print(field)
                    field = str(field)
                    field = field.replace('\n', '').replace('\r', '')
                    self._data.append(field)
                self._dataExport.append(self._data[:])
                self._data.clear()

            print(self._dataExport)

            # print(data)

            # empresas = pd.read_sql_query(sql, self._connection)

            # for empresa in empresas.values():
            #     print(empresa)

            # empresas.to_csv(self._caminhoSalvarCSV, header=True, sep='|',float_format='%g',decimal='.', encoding='Windows-1252', na_rep='(null)', index=None)
        except Exception as e:
            print(f"Erro ao executar a consulta. O erro é: {e}")
        finally:
            if self._cursor is not None:
                self._cursor.close()
            self._DB.closeConnection()


