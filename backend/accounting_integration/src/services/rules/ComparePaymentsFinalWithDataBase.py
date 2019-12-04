import sys
import os

fileDir = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(os.path.join(fileDir, 'backend'))
sys.path.append(os.path.join(fileDir, 'backend/accounting_integration/src/services'))

import json
from datetime import datetime, timedelta
from tools.leArquivos import leXls_Xlsx, leTxt
import tools.funcoesUteis as funcoesUteis
from read_files.PaymentsCDI import PaymentsCDI
from read_files.SispagItau import SispagItau
from read_files.ExtractsOFX import ExtractsOFX


class ComparePaymentsFinalWithDataBase(object):
    pass