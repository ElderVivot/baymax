import pandas as pd
import pyodbc
from db.ConexaoBanco import DB

class extractGeempre():
    def __init__(self):
        self._DB = DB()
        self._connection = self._DB.getConnection()
        self._cursor = None

    def exportaDados(self):
        try:
            self._cursor = self._connection.cursor()
            sql = ("SELECT * FROM bethadba.geempre ORDER BY codi_emp")
            self._cursor.execute(sql)

            empresas = pd.read_sql_query(sql, connect.con)
        except Exception as e:
            print(f"Erro ao executar a consulta. O erro é: {e}")
        finally:
            if self._cursor is not None:
                self._cursor.close()
            self._DB.closeConnection()


