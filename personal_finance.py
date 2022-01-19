import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import fsolve

class house_loan:
    """
    Functions to calculate monthly payment and mortgage schedules (for amortized mortgage)
    The monthly payment function is verified against https://www.mortgagecalculator.org/calcs/20-vs-30-year-mortgage.php#, and gives the exact same values to the cents
    Property tax is a simple percentage of the house price generally less than 1%
    """
    def __init__(self,house_price, down_payment, loan_term_years, annual_interest_rate, property_tax_annual_rate=0.):
        self.house_price = house_price
        self.down_payment = down_payment
        self.principal = self.house_price-self.down_payment
        self.loan_term_years = loan_term_years
        self.annual_interest_rate = annual_interest_rate
        self.property_tax_annual_rate = property_tax_annual_rate
    
    def calculate_balance_after_term(self,monthly_payment):
        balance = self.principal
        T = int(self.loan_term_years*12)
        monthly_interest_multiplier = self.annual_interest_rate/1200.
        amount_towards_interest = 0.
        amount_towards_balance = 0.
        for t in range(T):
            amount_towards_interest = monthly_interest_multiplier * balance
            amount_towards_balance = monthly_payment - amount_towards_interest
            balance = balance - amount_towards_balance
        return balance
    
    def calculate_monthly_payment(self):
        balance_function = lambda m : self.calculate_balance_after_term(m)
        result = fsolve(balance_function, 5000.)
        return result[0]
    
    def loan_specs(self, return_schedule=False):
        result = {}
        result["monthly_payment"] = self.calculate_monthly_payment()
        result["total_interest"] = result["monthly_payment"]*self.loan_term_years*12 - self.principal
        if self.property_tax_annual_rate>0.:
            result["monthly_payment_with_etc"] = result["monthly_payment"] + self.house_price*self.property_tax_annual_rate/1200.
        if return_schedule:
            balance = self.principal
            T = int(self.loan_term_years*12)
            mortgage_schedule = np.zeros((T,4))
            monthly_interest_multiplier = self.annual_interest_rate/1200.
            amount_towards_interest = 0.
            amount_towards_balance = 0.
            for t in range(T):
                amount_towards_interest = monthly_interest_multiplier * balance
                amount_towards_balance = result["monthly_payment"] - amount_towards_interest
                balance = balance - amount_towards_balance
                mortgage_schedule[t,0] = amount_towards_interest
                mortgage_schedule[t,1] = amount_towards_balance
                mortgage_schedule[t,2] = balance
                mortgage_schedule[t,3] = self.house_price*self.property_tax_annual_rate/1200.
            
            result["mortgage_schedule"] = pd.DataFrame(mortgage_schedule, columns=['Amount_towards_interest','Amount_towards_balance','Outstanding_balance','Tax_Insurance_etc'])
        return result

# Needs to be OOPified
def recurring_investment_returns(monthly_investment, term, annual_interest_rate):
    T = term*12
    total = 0.
    monthly_interest = annual_interest_rate/1200.
    for t in range(T):
        total += (total*monthly_interest + monthly_investment)
    
    return total


def alternate_investment_scenario(monthly_rent, rent_inflation_rate, market_investment_return_rate, house_loan_x, house_price_inflation_rate):
    loan_specs_data = house_loan_x.loan_specs(return_schedule=True)
    result = {}
    result["home_owner_scenario_wealth"] = house_loan_x.house_price*((1.+house_price_inflation_rate/100.)**house_loan_x.loan_term_years)
    result["renter_scenario_wealth"] = house_loan_x.down_payment
    mortgage_array = np.array([loan_specs_data["monthly_payment"]]*(house_loan_x.loan_term_years*12))
    rent_array = monthly_rent*np.repeat(np.power((1.+rent_inflation_rate/100.),np.arange(0.,house_loan_x.loan_term_years,1.)),12)
    for i in range(house_loan_x.loan_term_years*12):
        result["renter_scenario_wealth"] = result["renter_scenario_wealth"]*(1.+market_investment_return_rate/1200.) + (mortgage_array - rent_array)[i]
    
    return result


