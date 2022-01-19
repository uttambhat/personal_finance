import numpy as np
import matplotlib.pyplot as plt
from personal_finance import *

#====================================
# loan specs, monthly payments etc.
#====================================

house_loan_1 = house_loan(house_price=1.2e6, down_payment=2.e5, loan_term_years=30, annual_interest_rate=3., property_tax_annual_rate=0.7)
house_loan_1.loan_specs(return_schedule=True)




