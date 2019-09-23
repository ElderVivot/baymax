import os
from services.ProcessaXMLNota import ProcessaXMLNota

class MainFiscal:

    pasta = "D:\\temp\\xmls"

    for raiz, diretorios, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            caminhoArquivo = os.path.join(raiz,arquivo)
            if arquivo.upper().endswith(('.XML')):
                processaXMLNota = ProcessaXMLNota(caminhoArquivo)
            else:
                continue

if __name__ == '__main__':
    mainFiscal = MainFiscal() 
