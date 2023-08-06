from cpanlp.tax.income_tax import *

class PersonalIncomeTax(IncomeTax):
    def __init__(self, rate, base, deductions, exemptions):
        super().__init__(rate, base, deductions)
        self.exemptions = exemptions