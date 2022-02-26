from pymongo import MongoClient
import json
import os
import sys

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

from tools.leArquivos import readJson

envData = readJson(os.path.join(fileDir, 'backend/env.json'))
hostDatabase = envData['hostDatabase']

class ConnectMongo(object):

    def __init__(self, nameDB='baymax'):
        self._connection =  None
        self._selectDB = None
        self._nameDB = nameDB
        
    def getConnetion(self):
        if self._connection is None:
            try:
                self._connection = MongoClient(f'mongodb://{hostDatabase}:27017/') # conecta num cliente do MongoDB rodando na sua máquina
                self._selectDB = self._connection[self._nameDB]
            except Exception as e:
                print(f"** Não foi possível realizar a conexão. O erro é: {e}")
        return self._selectDB

    def closeConnection(self):
        if self._connection is not None:
            try:
                self._connection.close()
                #print('- Conexão fechada com sucesso')
            except Exception as e:
                print(f"** Não foi possível fechar a conexão. O erro é: {e}")


if __name__ == "__main__":
    connect = ConnectMongo()
    connect.getConnetion()