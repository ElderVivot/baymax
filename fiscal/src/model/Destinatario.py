class Destinatario(object):
    def __init__(self, cnpj, nome):
        self.__cnpj = cnpj
        self.__nome = nome

    @property
    def cnpj(self):
        return self.__cnpj

    @property
    def nome(self):
        return self.__nome
