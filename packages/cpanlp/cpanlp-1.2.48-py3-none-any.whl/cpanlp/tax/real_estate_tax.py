from cpanlp.tax.property_tax import *

class RealEstateTax(PropertyTax):
    def __init__(self, rate, base,deductions,value, square_footage):
        super().__init__(rate, base,deductions,value)
        self.square_footage = square_footage
