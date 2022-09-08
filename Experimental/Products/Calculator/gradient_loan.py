from decimal import Decimal
import pandas as pd
import numpy as np
import datetime as dt

from mortgage import Loan
from rsu_discounter import computeRsuValue

'''
    A loan object for Gradient's purposes.

    Wrapper around Loan class from mortgage library that includes additional
    mortgage related metrics (e.g. DTI, LTI, and LTV) and gradient
    adjusted metrics.
'''
class GradientLoan:

    # Avg Monthly Debt in California
    # https://www.lendingtree.com/personal/average-monthly-debt-payments-throughout-us/
    US_DEBT_MONTHLY_DOLLARS = 3500

    DEFAULT_FR_MORTGAGE_TERM_YEARS = 30 # Default Fixed Rate Mortgage Term

    # Default salary_income to 150K
    def __init__(self, salary_income=0, rsu_income=0, ticker='N/A', house_value_dollars=1e6, down_payment_percent=.2, interest_decimal=.058, term=DEFAULT_FR_MORTGAGE_TERM_YEARS):
        # Cast to decimal because loan class uses Decimal.
        self.salary_income = Decimal(salary_income)
        self.rsu_income = Decimal(rsu_income)
        self.house_value_dollars = house_value_dollars
        self.down_payment_percent = down_payment_percent
        self.interest_decimal = interest_decimal
        self.term = term
        self.ticker = ticker
        # Set discounted RSU value
        self.gradient_income = self.getGradientIncome()
        self.loan = self.getLoan()

    # Used for setting internal loan object
    def getLoan(self):
        principal = (1 - self.down_payment_percent) * self.house_value_dollars
        return Loan(principal=principal, interest=self.interest_decimal, term=self.term)

    def updateLoanInterest(self, interest_decimal):
        self.interest_decimal = interest_decimal
        self.loan = self.getLoan()

    # Get discounted RSU value
    def getGradientRsu(self):
        if self.ticker == 'N/A':
            return 0
        return computeRsuValue(self.ticker, self.rsu_income)

    # Get total income based on salary and discounted RSU value
    def getGradientIncome(self):
        if self.ticker == 'N/A':
            return self.salary_income
        return self.salary_income + self.getGradientRsu()

    # Get salary income
    def getSalaryIncome(self):
        return self.salary_income

    def getDownPaymentPercent(self):
        return self.down_payment_percent

    # Get APR as percent
    def getApr(self):
        return self.loan.apr

    def getInterest(self):
        return self.loan.interest

    def getTotalInterestDollars(self):
        return self.loan.total_interest

    def getPrincipal(self):
        return self.loan.principal

    def getMonthlyPayment(self):
        return self.loan.monthly_payment

    def getHouseValue(self):
        return self.house_value_dollars

    def getDebt(self):
        debt_without_rent = self.getDebtWithoutRent()
        return debt_without_rent + self.getMonthlyPayment()

    def getDebtWithoutRent(self):
        return self.US_DEBT_MONTHLY_DOLLARS - 1500 #1500 as arbitrary rent

    def getLtv(self):
        return self.loan.principal/self.house_value_dollars

    # Compute DTI using only salary income
    def getDti(self):
        monthly_income = self.salary_income/12
        if monthly_income < 100:
            # Failsafe in case user inputs $0 of income
            monthly_income = 100
        return self.getDebt()/monthly_income

    # Compute LTI using only salary income
    def getLti(self):
        if self.salary_income < 100:
            # Failsafe in case user inputs $0 of income
            self.salary_income = 100
        return self.loan.principal/self.salary_income

    ############ Gradient-adjusted attributes ############

    # Compute DTI using Gradient's income
    def getGradientDti(self):
        if self.ticker == 'N/A':
            # Check in case method called on loan without RSU income.
            return self.getDti()
        monthly_gradient_income = self.gradient_income/12
        if monthly_gradient_income < 100:
            monthly_gradient_income = 100
        return self.getDebt()/monthly_gradient_income

    # Compute LTI using Gradient's income
    def getGradientLti(self):
        if self.ticker == "N/A":
            # Check in case method called on loan without RSU income.
            return self.getLti()
        if self.gradient_income < 100:
            # Failsafe in case user inputs $0 of income
            return self.loan.principal/100
        return self.loan.principal/self.gradient_income
