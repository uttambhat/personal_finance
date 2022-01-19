import numpy as np
import matplotlib.pyplot as plt
from personal_finances import *

#================================================================================================
# Compare simple interest monthly payment with amortized payments for quick mental calculations
#================================================================================================
interest = 3.
principal = 1.e6
term_range = np.arange(1,31,1)
simple_interest = term_range*interest*principal/200.
actual_interest = [house_loan(house_price=principal, down_payment=0., loan_term_years=term, annual_interest_rate=interest).loan_specs()["total_interest"] for term in term_range]
plt.scatter(term_range,simple_interest,label="Simple interest")
plt.scatter(term_range,actual_interest,label="Actual interest")
plt.xlabel("loan term (years)")
plt.ylabel("Total interest")
plt.legend()
plt.show()

term = 30
interest_range = np.arange(2.5,5.1,0.1)
simple_interest = interest_range*term*principal/200.
actual_interest = [house_loan(house_price=principal, down_payment=0., loan_term_years=term, annual_interest_rate=interest).loan_specs()["total_interest"] for interest in interest_range]
plt.scatter(interest_range,simple_interest,label="Simple interest")
plt.scatter(interest_range,actual_interest,label="Actual interest")
plt.xlabel("interest rate (percent/year)")
plt.ylabel("Total interest")
plt.legend()
plt.show()

