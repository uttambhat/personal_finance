import numpy as np
import matplotlib.pyplot as plt
from personal_finances import *

#================================================================================================
# Compare alternate investment scenarios - 1) rent and invest in market vs. 2) invest in a house
#================================================================================================

networth = alternate_investment_scenario(monthly_rent=3000., rent_inflation_rate=2., market_investment_return_rate=7., \
                              house_loan_x=house_loan(house_price=1200000., down_payment=200000., loan_term_years=30, annual_interest_rate=3., property_tax_annual_rate=0.7), house_price_inflation_rate=2.)

print("Net worth if renting after 30 years: ",networth['renter_scenario_wealth'])
print("Net worth if a home owner after 30 years: ",networth['home_owner_scenario_wealth'])




