from cpanlp.tax.turnover_tax import *

class VAT(TurnoverTax):
    def __init__(self, rate, base,deductions):
        super().__init__(rate, base,deductions)