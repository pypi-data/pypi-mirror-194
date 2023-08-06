from cpanlp.tax.tax import *

class TurnoverTax(Tax):
    def __init__(self, rate, base,deductions):
        super().__init__(rate, base,deductions)