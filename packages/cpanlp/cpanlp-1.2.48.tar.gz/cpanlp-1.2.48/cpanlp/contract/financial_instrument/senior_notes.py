from cpanlp.contract.financial_instrument.bond import *
class ConvertibleBond(Bond):
    
    def __init__(self, issuer=None, coupon=None, conversion_price=None, maturity_date=None,parties=None, 
consideration=None,obligations=None, value=None,rate=None,currency=None,domestic=None,date=None,
outstanding_balance=None):
        super().__init__(parties,value, rate, currency,domestic,date,consideration, obligations,outstanding_balance)
        
class SeniorNotes(Bond):
    """
    Senior notes are a type of debt security issued by a company or government agency. They are considered a type of bond, but with some unique features.

    Unlike traditional bonds, senior notes are unsecured, meaning they are not backed by any collateral. This means that if the issuer defaults on the debt, the senior note holders have no claim to any specific assets, but are instead paid out of the issuer's general funds.

    Despite being unsecured, senior notes are considered senior in the issuer's capital structure. This means that in the event of a default, senior note holders have priority over other unsecured creditors, but are subordinate to secured creditors, such as bondholders or lenders who have a lien on specific assets.

    Senior notes typically have a longer maturity than other types of debt, such as commercial paper or short-term notes. They are also typically offered at a higher interest rate to compensate for the higher risk to investors, as they lack collateral.

    Overall, senior notes are a type of unsecured bond that is subordinate to secured creditors but has a higher priority than other unsecured creditors in the event of a default. They are typically offered at a higher interest rate and have a longer maturity than other types of debt.
    """
    def __init__(self, issuer=None, amount=None,  maturity=None,parties=None,value=None, rate=None, currency=None,domestic=None,date=None,consideration=None, obligations=None,outstanding_balance=None):
        super().__init__(parties,value, rate, currency,domestic,date,consideration, obligations,outstanding_balance)
        self.issuer = issuer
        self.amount = amount
        self.maturity = maturity

    def get_issuer(self):
        return self.issuer

    def get_amount(self):
        return self.amount

    def get_maturity(self):
        return self.maturity

    def is_unsecured(self):
        return True

    def has_collateral(self):
        return False

    def get_priority(self):
        return "Senior"

    def get_subordination(self):
        return "Subordinate to secured creditors, but has priority over other unsecured creditors"

    def get_description(self):
        return "Senior notes are a type of unsecured bond that is subordinate to secured creditors, but has a higher priority than other unsecured creditors in the event of a default. They typically have a longer maturity than other types of debt and are offered at a higher interest rate to compensate for the lack of collateral."
