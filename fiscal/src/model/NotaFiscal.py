from .Emitente import Emitente
from .Destinatario import Destinatario

class NotaFiscal(object):
    def __init__(self, chaveNF, numeroNF, valorNF, dataEmissaoNF, modeloNF ):
        self.__chaveNF = chaveNF
        self.__numeroNF = numeroNF
        self.__valorNF = valorNF
        self.__dataEmissaoNF = dataEmissaoNF
        self.__modeloNF = modeloNF
        self.__emitente = None
        self.__destinatario = None

    # @__destinatario.setter
    # def setDestinatario(destinatario):
    #     self.__destinatario = destinatario

    # @property
    # def getDestinatario():
    #     return self.__destinatario


