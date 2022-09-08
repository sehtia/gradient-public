from decimal import Decimal
import pandas as pd
import numpy as np
import datetime as dt

from buying_power_optimizer import BuyingPowerOptimizer
from gradient_loan import GradientLoan
from mortgage import Loan

'''
    Computes the change in PD based on income change and determines how much
    discount should be applied to the APR.

    Indirectly based off
    https://scholar.harvard.edu/files/campbell/files/mortdefault13022014.pdf

    TODO: Needs to be cleaned up
'''
class LoanRiskProcessor:

    # constructor
    def __init__(self, salary_income, rsu_income, rsu_ticker, house_value_dollars):
        # Update loans to be based on runtime APR
        self.gradient_loan = GradientLoan(salary_income, rsu_income, rsu_ticker, house_value_dollars)
        self.control_loan = GradientLoan(salary_income=salary_income, house_value_dollars=house_value_dollars)

    # Get change in PD based on salary only
    def getSalaryPdDelta(self):
        return Decimal(.055) * self.gradient_loan.getLti()

    # Get change in PD based on total income (salary + rsu)
    # [.033 - .055] * LTI = Reduction in PD a.k.a Delta(PD)
    def getTotalIncomePdDelta(self):
        print("LTI: %f" % self.gradient_loan.getGradientLti())

        pd_delta = Decimal(.055) * self.gradient_loan.getGradientLti()

        # if (pd_delta > .5):
        #     return Decimal(.5)
        # if (pd_delta < 0):
        #     return Decimal(0.000001)
        return pd_delta

    # Get change in rate
    # Delta(Rate) = Delta(PD) * (1 - LTV)
    # LTV is proxy for recovery rate. Recovery rate is from mortgage bonds
    # DO NOT USE
    # def getRateDelta(self):
    #     rate_delta = self.getTotalIncomePdDelta() * (1 - self.gradient_loan.getLtv())
    #     # Max rate decrease is 1% (arbitrary)
    #     if rate_delta > 1.0:
    #         return Decimal(1.0)
    #     return rate_delta

    # TODO add validation on income
    def getRateDeltaBucketed(self, pd_delta):
        #pd_delta = self.getTotalIncomePdDelta()
        print("pd delta: %f" % pd_delta)
        # Rate delta is how much income change impacts
        # The closer pd_delta gets to .5, the closer you are to a .015 discount.
        rate_delta_upper_bucket = Decimal(.5)
        rate_delta_lower_bucket = Decimal(0.0)
        # Discount is for range of discount that can be applied
        discount_upper_bucket = Decimal(.015)
        discount_lower_bucket = Decimal(0.0)

        rate_delta_bucket_range = rate_delta_upper_bucket - rate_delta_lower_bucket
        discount_bucket_range = discount_upper_bucket - discount_lower_bucket
        pd_delta_bucket = rate_delta_upper_bucket - pd_delta
        print("rate delta bucket: %f" % rate_delta_bucket_range)
        print("discount_bucket_range: %f" % discount_bucket_range)
        print("pd_delta_bucket: %f" % pd_delta_bucket)
        # pd_delta is Decimal, so we need to cast
        rate_delta_bucket = (pd_delta_bucket / rate_delta_bucket_range) * discount_bucket_range

        rate_delta_old = (pd_delta / rate_delta_bucket_range) * discount_bucket_range
        print("rate_delta_old: %f" % rate_delta_old)
        print("rate delta bucket: %f" % rate_delta_bucket)

        # In case someone has a very low or very high salary, limit discount.
        # E.g. $20K income or $20M income lmao.
        # We don't want to change discount_upper_bucket to match below because
        # that impacts difference between Gradient APR and traditional APR.
        if (rate_delta_bucket > discount_upper_bucket):
            return discount_upper_bucket
        if (rate_delta_bucket < discount_lower_bucket):
            return discount_lower_bucket

        return rate_delta_bucket

    # Compute Gradient's discounted APR
    # DO NOT USE
    # def getGradientApr(self):
    #     interest = self.control_loan.getInterest() - self.getRateDelta()
    #     return interest*100

    # Compute Gradient's discounted, bucketed APR
    def getGradientAprBucketed(self):
        print("interest loan original: %f" % self.control_loan.getInterest())
        total_income_rate_delta = self.getRateDeltaBucketed(self.getTotalIncomePdDelta())
        interest = self.control_loan.getInterest() - total_income_rate_delta
        # if (self.gradient_loan.getGradientIncome() == self.gradient_loan.salary_income):
        #     return interest*100
        # interest = self.getSalaryApr()/100 - total_income_rate_delta
        # print("apr is: %f" % interest)
        return interest*100

    # Get's APR based on salary income only
    def getSalaryApr(self):
        total_income_rate_delta = self.getRateDeltaBucketed(self.getSalaryPdDelta())
        # total_income_rate_delta = self.getSalaryRateDeltaBucketed()
        interest = self.control_loan.getInterest() - total_income_rate_delta
        return interest*100

    # TODO add savings
    def computeDifferentials(self):
        gradient_apr = round(self.getGradientAprBucketed(), 2)
        gradient_interest = gradient_apr/100
        gradient_principal = self.gradient_loan.getPrincipal()
        print(f"gradient_principal: {gradient_principal}")
        # gradient_apr_loan = Loan(principal=gradient_principal, interest=gradient_interest, term=30)
        # self.gradient_loan.setLoan(gradient_apr_loan)
        self.gradient_loan.updateLoanInterest(gradient_interest)

        salary_apr = round(self.getSalaryApr(), 2)
        salary_interest = salary_apr/100
        control_principal = self.control_loan.getPrincipal()
        print(f"control principal: {control_principal}")
        self.control_loan.updateLoanInterest(salary_interest)
        # traditional_salary_apr_loan = Loan(principal=control_principal, interest=salary_interest, term=30)
        # self.control_loan.setLoan(traditional_salary_apr_loan)


        gradient_traditional_interest_dollars = self.gradient_loan.getTotalInterestDollars()#gradient_apr_loan.total_interest
        traditional_interest_dollars = self.control_loan.getTotalInterestDollars() #traditional_salary_apr_loan.total_interest
        monthly_payment = self.control_loan.getMonthlyPayment()
        gradient_monthly_payment = self.gradient_loan.getMonthlyPayment()
        # GradientLoan attributes
        gradient_rsu = round(self.gradient_loan.getGradientRsu(), 2)
        dti = round(self.control_loan.getDti(), 2)
        gradient_dti = round(self.gradient_loan.getGradientDti(), 2)

        # Get maximum house size.
        buying_power_optimizer = BuyingPowerOptimizer(salary_interest)
        house_values = buying_power_optimizer.getDtiLoanSizes(\
            self.control_loan.getSalaryIncome(),\
            self.gradient_loan.getGradientRsu(), \
            self.gradient_loan.getDownPaymentPercent())
        traditional_max_loan_size = round(house_values[0])
        gradient_max_loan_size = round(house_values[1])

        return self._computeDifferentials(\
            gradient_rsu, \
            salary_apr, \
            gradient_apr, \
            dti, \
            gradient_dti, \
            traditional_interest_dollars, \
            gradient_traditional_interest_dollars,
            monthly_payment,
            gradient_monthly_payment,
            traditional_max_loan_size,
            gradient_max_loan_size)

    # Return dictionary of differentials
    def _computeDifferentials(self, \
        gradient_rsu, \
        traditional_apr, \
        gradient_apr, \
        traditional_dti, \
        gradient_dti, \
        traditional_interest_dollars, \
        gradient_traditional_interest_dollars, \
        monthly_payment, \
        gradient_monthly_payment, \
        traditional_max_loan_size, \
        gradient_max_loan_size):
        interest_saved_dollars = traditional_interest_dollars - gradient_traditional_interest_dollars
        return {
            'TraditionalRsu': 0,
            'GradientRsu': gradient_rsu,
            'TraditionalApr': traditional_apr,
            'GradientApr': gradient_apr,
            'TraditionalDti': traditional_dti,
            'GradientDti': gradient_dti,
            'TraditionalTotalInterestDollars': traditional_interest_dollars,
            'GradientTotalInterestDollars': gradient_traditional_interest_dollars,
            'InterestSavedDollars': interest_saved_dollars,
            'MonthlyPayment': monthly_payment,
            'GradientMonthlyPayment': gradient_monthly_payment,
            'TraditionalMaxLoanValue': traditional_max_loan_size,
            'GradientMaxLoanValue': gradient_max_loan_size
        }


# memorial tuesday morning at 9am at temple

'''
Requirements:

Inputs: ticker


company drop down -> ticker -> RSU haircut
title -> RSU, income
city -> proxy for rates (looks more dynamic for traditional apr)

----

0) Get gradient income from IV
1) LTI

2) Get change in PD

[.033 - .055] * LTI = Reduction in PD a.k.a Delta(PD)
^ anyway to flex this?

3) Get Change in Rate spread
LTV is proxy for recovery rate. Recovery rate is from mortgage bonds

Delta(Rate) = Delta(PD) * (1 - LTV)

4) Gradient Rate = Competitor - Delta(Rate)

Assumption: Using risk model from harvard bruh
Assumption: LTV is proxy for recovery rate. Recovery rate is from mortgage bonds
Assumption: Use bottom of weight in (2) since we are using .8 LTV.

Example:

Salary = 100K and RSU=100K
Gradient Total Income = 200K (RSU + Salary)

DTI:
Traditional = (3+mortgage_payment)/8.3 = .36
Gradient = (3+mortgage_payment)/16.3 = .18

Rate Calc:
LTI = 800/200 = 4
Delta(PD) = .033 * 4 = .132
LTV = 800/1M
Delta(Rate Spread) = .132 * .2 = .0264

-- Need some safe threshold for discounting. Maximum of 1%
--

City Avg Mortgage Rate = 5.5
5.5 - .0264 = 5.47

'''
