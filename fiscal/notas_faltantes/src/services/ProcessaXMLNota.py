from model.Emitente import Emitente
from model.Destinatario import Destinatario
from model.NotaFiscal import NotaFiscal
import xmltodict as xmldict

class ProcessaXMLNota(object):
    def __init__(self, xml):
        # lê o xml
        with open(xml) as fd:
            xmlDados = xmldict.parse(fd.read())

        # instancia os dados
        self.__chaveNota = ProcessaXMLNota.setChaveNota(xmlDados)
        self.__NumeroNota = ProcessaXMLNota.setNumeroNota(xmlDados)
        self.__emissaoNota = ProcessaXMLNota.setEmissaoNota(xmlDados)
        self.__modeloNota = ProcessaXMLNota.setModeloNota(xmlDados)
        self.__valorNota = ProcessaXMLNota.setValorNota(xmlDados)
        self.__valorICMS = ProcessaXMLNota.setValorICMS(xmlDados)
        self.__cnpjEmitente = ProcessaXMLNota.setCNPJEmitente(xmlDados)
        self.__nomeEmitente = ProcessaXMLNota.setNomeEmitente(xmlDados)
        self.__cnpjDestinatario = ProcessaXMLNota.setCNPJDestinatario(xmlDados)
        self.__nomeDestinatario = ProcessaXMLNota.setNomeDestinatario(xmlDados)

        # instancia os objs
        self.__emitente = Emitente(self.__cnpjEmitente, self.__nomeEmitente)

        self.__destinatario = Destinatario(self.__cnpjDestinatario, self.__nomeDestinatario)

        self.__notaFiscal = NotaFiscal(self.__chaveNota, self.__NumeroNota, self.__emissaoNota, self.__modeloNota,\
            self.__valorNota, self.__valorICMS, self.__emitente, self.__destinatario)

    @staticmethod
    def setChaveNota(xml):
        try:
            chaveNota = xml['nfeProc']['NFe']['infNFe']['@Id']
            chaveNota = chaveNota[3:]
        except Exception:
            chaveNota = None

        return chaveNota

    @staticmethod
    def setNumeroNota(xml):
        try:
            numeroNota = xml['nfeProc']['NFe']['infNFe']['ide']['nNF']
        except Exception:
            numeroNota = None

        return numeroNota

    @staticmethod
    def setEmissaoNota(xml):
        try:
            emissao = xml['nfeProc']['NFe']['infNFe']['ide']['dhEmi']
            emissao = emissao[0:10]
        except Exception:
            emissao = None

        return emissao

    @staticmethod
    def setModeloNota(xml):
        try:
            modelo = xml['nfeProc']['NFe']['infNFe']['ide']['mod']
        except Exception:
            modelo = None

        return modelo

    @staticmethod
    def setValorNota(xml):
        try:
            valorNota = xml['nfeProc']['NFe']['infNFe']['total']['ICMSTot']['vNF']
        except Exception:
            valorNota = None

        return valorNota

    @staticmethod
    def setValorICMS(xml):
        try:
            valorICMS = xml['nfeProc']['NFe']['infNFe']['total']['ICMSTot']['vICMS']
        except Exception:
            valorICMS = None

        return valorICMS

    @staticmethod
    def setCNPJEmitente(xml):
        try:
            cnpjEmitente = xml['nfeProc']['NFe']['infNFe']['emit']['CNPJ']
        except Exception:
            cnpjEmitente = None

        return cnpjEmitente

    @staticmethod
    def setNomeEmitente(xml):
        try:
            nomeEmitente = xml['nfeProc']['NFe']['infNFe']['emit']['xNome']
        except Exception:
            nomeEmitente = None

        return nomeEmitente

    @staticmethod
    def setCNPJDestinatario(xml):
        try:
            cnpjDestinario = xml['nfeProc']['NFe']['infNFe']['dest']['CNPJ']
        except Exception:
            cnpjDestinario = None

        try:
            cpfDestinario = xml['nfeProc']['NFe']['infNFe']['dest']['CPF']
        except Exception:
            cpfDestinario = None

        if cnpjDestinario is None:
            cnpjDestinario = cpfDestinario

        if cnpjDestinario is None:
            cnpjDestinario = '99999999999'

        return cnpjDestinario

    @staticmethod
    def setNomeDestinatario(xml):
        try:
            nomeDestinatario = xml['nfeProc']['NFe']['infNFe']['dest']['xNome']
        except Exception:
            nomeDestinatario = 'SEM NOME DEFINIDO PRO DESTINATÁRIO'

        return nomeDestinatario

    @property
    def notaFiscal(self):
        return self.__notaFiscal      