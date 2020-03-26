import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import json
import tools.funcoesUteis as funcoesUteis
from dao.src.ConnectMongo import ConnectMongo
from bson.objectid import ObjectId

class GetSettingsCompany(object):

    def __init__(self, codiEmp):
        self._codiEmp = codiEmp

        self._connectionMongo = ConnectMongo()
        self._dbMongo = self._connectionMongo.getConnetion()
        self._collection = self._dbMongo.IntegrattionCompanies

    def getSettingsLayout(self, layouts):
        settingsLayouts = []
        try:
            collectionLayouts = self._dbMongo.IntegrattionLayouts

            for layout in layouts:
                idLayout = funcoesUteis.analyzeIfFieldIsValid(layout, 'idLayout', None)

                settings = collectionLayouts.find_one( { "_id": ObjectId(idLayout) } )

                bankAndAccountCorrelation = funcoesUteis.analyzeIfFieldIsValid(layout, 'bankAndAccountCorrelation', None)
                validateIfDataIsThisCompanie = funcoesUteis.analyzeIfFieldIsValid(layout, 'validateIfDataIsThisCompanie', None)

                if settings is not None:
                    settings['bankAndAccountCorrelation'] = bankAndAccountCorrelation
                    settings['validateIfDataIsThisCompanie'] = validateIfDataIsThisCompanie
                    settingsLayouts.append(settings)

        except Exception:
            pass

        return settingsLayouts
    
    def getSettingsFinancy(self):
        try:
            settings = self._collection.find_one( { "codi_emp": self._codiEmp } )

            layouts = funcoesUteis.returnDataFieldInDict(settings, ['financy', 'layouts'])

            settingsLayouts = self.getSettingsLayout(layouts)

            settings['settingsLayouts'] = settingsLayouts
        except Exception:
            settings = None
        finally:
            self._connectionMongo.closeConnection()

        return settings


if __name__ == "__main__":
    getSettingsCompany = GetSettingsCompany(1342)
    print(getSettingsCompany.getSettingsFinancy())