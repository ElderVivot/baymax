from pymongo import MongoClient


class ConnectMongo(object):

    def __init__(self, nameDB='baymax'):
        self._connection =  None
        self._selectDB = None
        self._nameDB = nameDB
        
    def getConnetion(self):
        if self._connection is None:
            try:
                self._connection = MongoClient('mongodb://192.168.254.227:27017/') # conecta num cliente do MongoDB rodando na sua máquina
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

    def testFunctionPymongo(self):
        self._collection = self._selectDB.teste
        self._collection.aggregate()


if __name__ == "__main__":
    connect = ConnectMongo()
    connect.getConnetion()