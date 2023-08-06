from cpanlp.tax.tax import *
class BehaviorTax(Tax):
    def __init__(self, rate, base,deductions,amount):
        super().__init__(rate, base,deductions)
        self.amount = amount
    @property
    def tax(self):
        return self.amount * self.rate