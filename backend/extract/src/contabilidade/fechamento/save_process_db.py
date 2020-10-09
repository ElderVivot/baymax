import os
import sys

absPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(absPath[:absPath.find('extract')])

from dao.src.ConnectMongo import ConnectMongo

class SaveProcessDb():
    def __init__(self, dataToSave):
        self._dataTosave = dataToSave

        self._connectionMongo = ConnectMongo()
        self._dbMongo = self._connectionMongo.getConnetion()
        self._collection = self._dbMongo['AccountFechamento']

    def save(self):
        try:
            self._collection.update_one( 
                { 
                    "codi_emp": self._dataTosave['codi_emp'],
                    "competence": self._dataTosave['competence']
                }, 
                { "$set": self._dataTosave }, 
                upsert=True 
            )
                        
        except Exception as e:
            print(f"Erro ao executar a consulta. O erro é: {e}")
        finally:
            self._connectionMongo.closeConnection()
