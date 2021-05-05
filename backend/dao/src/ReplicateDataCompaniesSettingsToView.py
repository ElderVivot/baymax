import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
fileDir = absPath[:absPath.find('backend')]
sys.path.append(os.path.join(fileDir, 'backend'))

import json
import tools.funcoesUteis as funcoesUteis
from dao.src.ConnectMongo import ConnectMongo
from bson.objectid import ObjectId

class ReplicateDataCompaniesSettingsToView(object):

    def __init__(self):
        self._connectionMongo = ConnectMongo()
        self._dbMongo = self._connectionMongo.getConnetion()
        self._collectionCompaniesSettings = self._dbMongo.CompaniesSettings
        self._collectionCompaniesSettingsView = self._dbMongo.CompaniesSettingsView

    def makeSaveData(self, data):
        obj = {
            "codi_emp": funcoesUteis.analyzeIfFieldIsValid(data, 'codi_emp'),
            "statusAccountPaid": funcoesUteis.analyzeIfFieldIsValid(data, 'statusAccountPaid'),
            "responsibleFinancialClient": funcoesUteis.analyzeIfFieldIsValid(data, 'responsibleFinancialClient'),
            "layoutsAccountPaid": funcoesUteis.analyzeIfFieldIsValid(data, 'layoutsAccountPaid'),
            "dateAccountPaid": funcoesUteis.analyzeIfFieldIsValid(data, 'dateAccountPaid'),
            "analystReceivedTraining": funcoesUteis.analyzeIfFieldIsValid(data, 'analystReceivedTraining'),
            "emailAccountPaid": funcoesUteis.analyzeIfFieldIsValid(data, 'emailAccountPaid'),
            "telefoneAccountPaid": funcoesUteis.analyzeIfFieldIsValid(data, 'telefoneAccountPaid'),
            "obsAccountPaid": funcoesUteis.analyzeIfFieldIsValid(data, 'obsAccountPaid')
        }
        return obj

    def process(self):
        try:
            dataCompaniesSettings = self._collectionCompaniesSettings.find()
            for data in dataCompaniesSettings:
                dataCompaniesSettingsView = self._collectionCompaniesSettingsView.find_one({"codi_emp": data['codi_emp']})
                self._collectionCompaniesSettings.update_one(
                    { "codi_emp": data['codi_emp'] },
                    { "$set": self.makeSaveData(dataCompaniesSettingsView) }
                )
        except Exception as e:
            print(e)
        finally:
            self._connectionMongo.closeConnection()


if __name__ == "__main__":
    main = ReplicateDataCompaniesSettingsToView()
    main.process()