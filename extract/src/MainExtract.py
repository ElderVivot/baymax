# encoding: utf-8

from geral.geempre import extractGeempre
from fiscal.efentradas import extractEfentradas
from fiscal.efmvepro import extractEfmvepro

class MainExtract:

    # geempre = extractGeempre()
    # geempre.exportaDados()

    efentradas = extractEfentradas()
    efentradas.exportaDados()

    # efmvepro = extractEfmvepro()
    # efmvepro.exportaDados()

if __name__ == '__main__':
    mainExtract = MainExtract() 