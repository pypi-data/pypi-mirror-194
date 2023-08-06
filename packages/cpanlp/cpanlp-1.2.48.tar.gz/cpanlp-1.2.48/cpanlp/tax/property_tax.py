from cpanlp.tax.tax import *

class PropertyTax(Tax):
    def __init__(self, rate, base,deductions,value):
        super().__init__(rate, base,deductions)
        self.value = value
    @property
    def tax(self):
        return self.value * self.rate