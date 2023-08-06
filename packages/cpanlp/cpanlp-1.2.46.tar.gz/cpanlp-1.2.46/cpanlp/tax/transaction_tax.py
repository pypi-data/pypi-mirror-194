from cpanlp.tax.behavior_tax import *

class TransactionTax(BehaviorTax):
    def __init__(self, rate, base,deductions,amount, transaction):
        super().__init__(rate, base,deductions,amount)
        self.transaction = transaction
    @property
    def tax(self):
        base_tax = super().calculate_tax()
        return base_tax + (self.transaction * 0.05)