# encoding: utf-8

from geral.geempre import extractGeempre
from fiscal.efentradas import extractEfentradas
from fiscal.efmvepro import extractEfmvepro
from fiscal.effornece import extractEffornece
from fiscal.efentradaspar import extractEfentradaspar

class MainExtract:

    geempre = extractGeempre()
    geempre.exportData()

    effornece = extractEffornece()
    effornece.exportData()

    efentradas = extractEfentradas()
    efentradas.exportData()

    efentradaspar = extractEfentradaspar()
    efentradaspar.exportData()

    # efmvepro = extractEfmvepro()
    # efmvepro.exportaDados()

if __name__ == '__main__':
    mainExtract = MainExtract() 