# coding: utf-8

import pyodbc

user='EXTERNO'
password='dominio'
host='Contabil'
port='2638'

class DB():

    def __init__(self):
        self.connection = None

    #@staticmethod
    def getConnection(self):
        if self.connection is None:
            try:
                self.connection = pyodbc.connect(DSN=host,UID=user,PWD=password,PORT=port)
                #print('- Conexão com a Domínio realizada com sucesso.')
            except Exception as e:
                print(f"** Não foi possível realizar a conexão. O erro é: {e}")
        return self.connection

    #@staticmethod
    def closeConnection(self):
        if self.connection is not None:
            try:
                self.connection.close()
                #print('- Conexão fechada com sucesso')
            except Exception as e:
                print(f"** Não foi possível fechar a conexão. O erro é: {e}")