from pymongo import MongoClient

nameDB = 'baymax'


class ConnectMongo(object):

    def __init__(self):
        self._connection =  None
        self._selectDB = None
        
    def getConnetion(self):
        if self._connection is None:
            try:
                self._connection = MongoClient() # conecta num cliente do MongoDB rodando na sua máquina
                self._selectDB = self._connection.baymax
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

    def testFunctionPymongo(self):
        self._collection = self._selectDB.teste
        self._collection.aggregate()