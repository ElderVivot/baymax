import sys
import os

absPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(absPath[:absPath.find('extract')])

import tools.funcoesUteis as funcoesUteis

class PagamentoConvenio(object):
    def __init__(self, dataFile):
        self._dataFile = dataFile

    def process(self):
        valuesOfLine = {}

        isPagamentoConvenio = False

        nameProvider = ""
        historic = ""
        amountPaid = float(0)
        account = ""
        amountOriginal = float(0)
        amountDiscount = float(0)
        amountInterest = float(0)
        amountFine = float(0)
        paymentDate = None
        dueDate = None
        
        for data in self._dataFile:
            if isPagamentoConvenio == False and data.find('COMPROVANTE DE PAGAMENTO') >= 0 and ( data.find('CONVENIO') or data.find('FGTS') ):
                isPagamentoConvenio = True

            data = str(data)
            dataSplit = data.split(':')

            fieldOne = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 1))
            fieldTwo = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 2))
            fieldThree = funcoesUteis.treatTextField(funcoesUteis.analyzeIfFieldIsValidMatrix(dataSplit, 3))
            
            if fieldOne.count('DO DOCUMENTO') > 0 and fieldTwo.count("DATA") > 0:
                paymentDate = funcoesUteis.retornaCampoComoData(fieldThree)

            if fieldOne == 'CONTA':
                account = funcoesUteis.treatNumberField(fieldTwo)

            if fieldOne == 'BENEFICIARIO':
                nameProvider = fieldTwo    

            if fieldOne == "VALOR DO DOCUMENTO":
                amountOriginal = funcoesUteis.treatDecimalField(fieldTwo)
            if fieldOne == 'ENCARGOS':
                amountInterest = funcoesUteis.treatDecimalField(fieldTwo)
            if fieldOne == "VALOR PAGO":
                amountPaid = funcoesUteis.treatDecimalField(fieldTwo)
            if fieldOne == "VALOR DO DESCONTO":
                amountDiscount = funcoesUteis.treatDecimalField(fieldTwo)

            if fieldOne == "VALOR PAGO":
                if paymentDate is not None and amountPaid > 0 and isPagamentoConvenio is True:
                    valuesOfLine = {
                        "paymentDate": paymentDate,
                        "nameProvider": nameProvider,
                        "cgceProvider": "",
                        "dueDate": dueDate,
                        "bank": 'AMAZONIA',
                        "account": account,
                        "amountPaid": round(amountPaid, 2),
                        "amountInterest": round(amountInterest, 2),
                        "amountDiscount": round(amountDiscount, 2),
                        "amountFine": round(amountFine, 2),
                        "amountOriginal": round(amountOriginal, 2),
                        "historic": historic,
                        "category": 'PAGAMENTO',
                        "cgcePaying": "",
                        "foundProof": True,
                        "amountPaidPerLote": round(amountPaid, 2)
                    }

                    return valuesOfLine.copy()