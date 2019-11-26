# encoding: utf-8

from geral.geempre import extractGeempre
from fiscal.efentradas import extractEfentradas

class MainExtract:

    # geempre = extractGeempre()
    # geempre.exportaDados()

    efentradas = extractEfentradas()
    efentradas.exportaDados()

if __name__ == '__main__':
    mainExtract = MainExtract() 