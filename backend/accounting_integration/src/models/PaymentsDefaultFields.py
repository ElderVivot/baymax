import os
import sys

fileDir = os.path.dirname(__file__)
sys.path.append(fileDir)

from ConfigurationsField import ConfigurationsField


class PaymentsDefaultFields(object):
    def __init__(self, paymentDate, amountPaid, document='', nameProvider='', cnpjProvider='', issuanceDate=None, dueDate=None, bank='', amountDiscount=0,\
        amountInterest=0, amountFine=0, historic='', category='', paymentType='', costCenter='', accountPlan=''):
         self.__document = document
         self.__nameProvider = nameProvider
         self.__cnpjProvider = cnpjProvider
         self.__issuanceDate = issuanceDate
         self.__dueDate = dueDate
         self.__paymentDate = paymentDate
         self.__bank = bank
         self.__amountPaid = amountPaid
         self.__amountDiscount = amountDiscount
         self.__amountInterest = amountInterest
         self.__amountFine = amountFine
         self.__historic = historic
         self.__category = category
         self.__paymentType = paymentType
         self.__costCenter = costCenter
         self.__accountPlan = accountPlan

    @property
    def document(self):
        return self.__document

    @document.setter
    def document(self, document):
        self.__document = document

    @property
    def nameProvider(self):
        return self.__nameProvider

    @nameProvider.setter
    def nameProvider(self, nameProvider):
        self.__nameProvider = nameProvider

    @property
    def cnpjProvider(self):
        return self.__cnpjProvider

    @cnpjProvider.setter
    def cnpjProvider(self, cnpjProvider):
        self.__cnpjProvider = cnpjProvider

    @property
    def issuanceDate(self):
        return self.__issuanceDate

    @issuanceDate.setter
    def issuanceDate(self, issuanceDate):
        self.__issuanceDate = issuanceDate

    @property
    def dueDate(self):
        return self.__dueDate

    @dueDate.setter
    def dueDate(self, dueDate):
        self.__dueDate = dueDate

    @property
    def paymentDate(self):
        return self.__paymentDate

    @paymentDate.setter
    def paymentDate(self, paymentDate):
        self.__paymentDate = paymentDate

    @property
    def bank(self):
        return self.__bank

    @bank.setter
    def bank(self, bank):
        self.__bank = bank

    @property
    def amountPaid(self):
        return self.__amountPaid

    @amountPaid.setter
    def amountPaid(self, amountPaid):
        self.__amountPaid = amountPaid

    @property
    def amountDiscount(self):
        return self.__amountDiscount

    @amountDiscount.setter
    def amountDiscount(self, amountDiscount):
        self.__amountDiscount = amountDiscount

    @property
    def amountInterest(self):
        return self.__amountInterest

    @amountInterest.setter
    def amountInterest(self, amountInterest):
        self.__amountInterest = amountInterest

    @property
    def amountFine(self):
        return self.__amountFine

    @amountFine.setter
    def amountFine(self, amountFine):
        self.__amountFine = amountFine

    @property
    def historic(self):
        return self.__historic

    @historic.setter
    def historic(self, historic):
        self.__historic = historic

    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self, category):
        self.__category = category

    @property
    def paymentType(self):
        return self.__paymentType

    @paymentType.setter
    def paymentType(self, paymentType):
        self.__paymentType = paymentType

    @property
    def costCenter(self):
        return self.__costCenter

    @costCenter.setter
    def costCenter(self, costCenter):
        self.__costCenter = costCenter

    @property
    def accountPlan(self):
        return self.__accountPlan

    @accountPlan.setter
    def accountPlan(self, accountPlan):
        self.__accountPlan = accountPlan