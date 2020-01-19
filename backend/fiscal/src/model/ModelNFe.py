from .Issuer import Issuer
from .Receiver import Receiver

class ModelNFe(object):
    def __init__(self, obj):
        self._obj = obj
        self._keyNF = self._obj["keyNF"]
        self._numberNF = self._obj["numberNF"]
        self._issueDateNF = self._obj["issueDateNF"]
        self._modelNF = self._obj["modelNF"]
        self._serieNF = self._obj["serieNF"]
        self._valueNF = self._obj["valueNF"]
        self._valueICMS = self._obj["valueICMS"]
        self._issuer = self._obj["issuer"]
        self._receiver = self._obj["receiver"]

    @property
    def keyNF(self):
        return self._keyNF

    @property
    def numberNF(self):
        return self._numberNF

    @property
    def issueDateNF(self):
        return self._issueDateNF

    @property
    def modelNF(self):
        return self._modelNF

    @property
    def serieNF(self):
        return self._serieNF

    @property
    def valueNF(self):
        return self._valueNF

    @property
    def valueICMS(self):
        return self._valueICMS

    @property
    def issuer(self):
        return self._issuer

    @property
    def receiver(self):
        return self._receiver


