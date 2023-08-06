from cpanlp.tax.tax import *

class IncomeTax(Tax):
    def __init__(self, rate, base, deductions):
        super().__init__(rate, base,deductions)
    def calculate(self, income):
        taxable_income = income - self.deductions
        return taxable_income * self.rate + self.base       