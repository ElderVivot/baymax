from .Emitente import Emitente
from .Destinatario import Destinatario

class NotaFiscal(object):
    def __init__(self, chaveNF, numeroNF, dataEmissaoNF, modeloNF, valorNF, valorICMS, emitente, destinatario):
        self.__chaveNF = chaveNF
        self.__numeroNF = numeroNF
        self.__dataEmissaoNF = dataEmissaoNF
        self.__modeloNF = modeloNF
        self.__valorNF = valorNF
        self.__valorICMS = valorICMS
        self.__emitente = emitente
        self.__destinatario = destinatario

    @property
    def chaveNF(self):
        return self.__chaveNF

    @property
    def numeroNF(self):
        return self.__numeroNF

    @property
    def dataEmissaoNF(self):
        return self.__dataEmissaoNF

    @property
    def modeloNF(self):
        return self.__modeloNF

    @property
    def valorNF(self):
        return self.__valorNF

    @property
    def valorICMS(self):
        return self.__valorICMS

    @property
    def emitente(self):
        return self.__emitente

    @property
    def destinatario(self):
        return self.__destinatario


