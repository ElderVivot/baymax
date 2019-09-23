from model.Emitente import Emitente
from model.Destinatario import Destinatario
# from model.NotaFiscal import NotaFiscal
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
        self.__cnpjEmitente = ProcessaXMLNota.setCNPJEmitente(xmlDados)
        self.__nomeEmitente = ProcessaXMLNota.setNomeEmitente(xmlDados)
        self.__cnpjDestinatario = ProcessaXMLNota.setCNPJDestinatario(xmlDados)
        self.__nomeDestinatario = ProcessaXMLNota.setNomeDestinatario(xmlDados)

        # instancia os objs
        self.__emitente = Emitente(self.__cnpjEmitente, self.__nomeEmitente)

        self.__destinatario = Destinatario(self.__cnpjDestinatario, self.__nomeDestinatario)

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
            nomeDestinatario = 'CONSUMIDOR FINAL'

        return nomeDestinatario      