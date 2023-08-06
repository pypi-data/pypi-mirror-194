from cpanlp.tax.turnover_tax import *

class ConsumptionTax(TurnoverTax):
    def __init__(self, rate, base,deductions):
        super().__init__(rate, base,deductions)