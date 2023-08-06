from cpanlp.contract.financial_instrument.financial_instrument import *

class Bond(FinancialInstrument):
    def __init__(self,parties=None,value=None, rate=None, currency=None,domestic=None,date=None,consideration=None, obligations=None,outstanding_balance=None):
        super().__init__(parties, consideration,obligations, value)
        self.rate = rate
        self.currency = currency
        self.domestic = domestic
        self.outstanding_balance = outstanding_balance
        self.date=date
