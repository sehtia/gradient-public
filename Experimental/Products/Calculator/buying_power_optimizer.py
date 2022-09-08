import numpy_financial

from decimal import Decimal
from gradient_loan import GradientLoan
from mortgage import Loan

# Should these be represented as Decimals?
MAXIMUM_BACKEND_DTI = .45
TRADITIONAL_BACKEND_DTI = .36
MAXIMUM_FRONTEND_DTI = .30
TRADITIONAL_FRONTEND_DTI = .28
TERM_YEARS = 30
TERM_MONTHS = TERM_YEARS*12

MAXIMUM_HOUSE_VALUE = Decimal(3e6) # $3M max house value
MAXIMUM_DIFFERENCE_IN_HOUSE_VALUE = Decimal(5e5) # 500K

'''
    Output: Largest loan in dollars person can get from Gradient based on DTI.

    i.e. If we kept Gradient APR and traditional APR the same, how much more
    home could the borrower buy.
    TODO: Add tests and input validation
'''
class BuyingPowerOptimizer():

    def __init__(self, interest_decimal=.058):
        self.interest_decimal = interest_decimal

    def getDtiLoanSizes(self, salary_income, rsu_income, down_payment_percent):
        house_prices = self.getDtiHouseValues(salary_income, rsu_income)
        loan_percent = Decimal(1 - down_payment_percent)
        return tuple(house_price*loan_percent for house_price in house_prices)

    #TODO: This should be split into two methods
    def getDtiHouseValues(self, salary_income, rsu_income):
        salary_house_value = self.getDtiHouseValue(salary_income, 0)
        gradient_house_value = self.getDtiHouseValue(salary_income, rsu_income)

        # Keep difference between house values below 500K
        house_value_diff = gradient_house_value - salary_house_value
        if house_value_diff > MAXIMUM_DIFFERENCE_IN_HOUSE_VALUE:
            gradient_house_value = salary_house_value

        return (salary_house_value, gradient_house_value)


    # we can use vesting schedule to weight income for house walue
    # clean this up man
    def getDtiHouseValue(self, salary_income, rsu_income, rsu_vesting_years=5):
        # Get weights based on vesting schedule
        salary_years = TERM_YEARS - rsu_vesting_years
        rsu_house_value = (salary_income + rsu_income) * Decimal(TRADITIONAL_FRONTEND_DTI) * rsu_vesting_years
        salary_house_value = (salary_income) * Decimal(TRADITIONAL_FRONTEND_DTI) * salary_years
        house_value = rsu_house_value + salary_house_value

        if house_value > MAXIMUM_HOUSE_VALUE:
            return MAXIMUM_HOUSE_VALUE
        if house_value < 0:
            return 0
        return house_value

    def getTraditionalHouseValue(self, salary_income):
        return self.getExpectedHouseValue(salary_income, Decimal(self.interest_decimal), TRADITIONAL_BACKEND_DTI)

    def getGradientHouseValue(self, gradient_income):
        return self.getExpectedHouseValue(gradient_income, Decimal(self.interest_decimal), MAXIMUM_BACKEND_DTI)

    # Assumption is that person will stop paying rent and pay mortgage
    # Change in working captial.
    # Where are people putting their income? in savings
    # Try putting RSU only to see how much house they can get
    # Checking compounding rate for mortgage
    # numpy_financial needs to take float. Output should be decimal
    def getExpectedHouseValue(self, annual_income, interest_decimal, dti_limit_decimal):
        # Convert to float since numpy_financial don't take Decimal.
        debt_without_rent = GradientLoan().getDebtWithoutRent()
        max_morty_payment = (annual_income/12 * Decimal(dti_limit_decimal)) - debt_without_rent
        # This calc is from POV of lender so we get a negative value becuase
        # money is leaving the account.
        loan_value_dollars = -1*numpy_financial.pv(rate=interest_decimal/12, nper=TERM_MONTHS, pmt=max_morty_payment)
        return Decimal(loan_value_dollars)/Decimal(.8)


# Main method for running ad-hoc
def main():
    interest_decimal = .048
    BPO = BuyingPowerOptimizer(interest_decimal)

    print("------------------------")

    print(f"get dti house values: {BPO.getDtiHouseValues(240000,140000)}")
    print(f"get dti loan sizes: {BPO.getDtiLoanSizes(240000,140000,.2)}")

# Using the special variable
if __name__=="__main__":
    main()
