class Tax:
    def __init__(self, rate, base,deductions):
        self.rate = rate
        self.base = base
        self.deductions =deductions
        self.object=None
        self.payer=None
        self.incentives=None
        self.deadline=None
        self.location=None
        self.history = []