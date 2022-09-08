from decimal import Decimal

from loan_risk_processor import LoanRiskProcessor

import unittest

TWO_PLACES = Decimal(10) ** -2

GOOGLE_SALARY_INCOME = 2.4e5
GOOGLE_RSU_INCOME = 1.4e5
GOOGLE_TICKER = 'GOOG'
SAN_FRANCISCO_HOUSE_PRICE = 1.3e6

class LoanRiskProcessorTest(unittest.TestCase):


    def test_get_gradient_apr_bucketed(self):
        loanRiskProcessor = LoanRiskProcessor(
            salary_income=GOOGLE_SALARY_INCOME, \
            rsu_income=GOOGLE_RSU_INCOME, \
            rsu_ticker=GOOGLE_TICKER, \
            house_value_dollars=SAN_FRANCISCO_HOUSE_PRICE)

        gradient_apr = loanRiskProcessor.getGradientAprBucketed().quantize(TWO_PLACES)

        self.assertEqual(gradient_apr, Decimal(4.78).quantize(TWO_PLACES))


    def test_get_gradient_apr_with_zero_income_has_max_apr_threshold(self):
        loanRiskProcessor = LoanRiskProcessor(
            salary_income=0, \
            rsu_income=0, \
            rsu_ticker=GOOGLE_TICKER, \
            house_value_dollars=SAN_FRANCISCO_HOUSE_PRICE)

        gradient_apr = loanRiskProcessor.getGradientAprBucketed().quantize(TWO_PLACES)

        self.assertEqual(gradient_apr, Decimal(5.8).quantize(TWO_PLACES))

    def test_get_salary_apr_with_zero_income_has_max_apr_threshold(self):
        loanRiskProcessor = LoanRiskProcessor(
            salary_income=0, \
            rsu_income=0, \
            rsu_ticker=GOOGLE_TICKER, \
            house_value_dollars=SAN_FRANCISCO_HOUSE_PRICE)

        salary_apr = loanRiskProcessor.getSalaryApr().quantize(TWO_PLACES)

        self.assertEqual(salary_apr, Decimal(5.8).quantize(TWO_PLACES))

    def test_get_salary_apr_with_absurd_income_has_min_apr_threshold(self):
        loanRiskProcessor = LoanRiskProcessor(
            salary_income=1e8, \
            rsu_income=GOOGLE_RSU_INCOME, \
            rsu_ticker=GOOGLE_TICKER, \
            house_value_dollars=SAN_FRANCISCO_HOUSE_PRICE)

        salary_apr = loanRiskProcessor.getSalaryApr().quantize(TWO_PLACES)

        self.assertEqual(salary_apr, Decimal(4.3).quantize(TWO_PLACES))

    def test_get_gradient_apr_with_absurd_income_has_min_apr_threshold(self):
        loanRiskProcessor = LoanRiskProcessor(
            salary_income=GOOGLE_SALARY_INCOME, \
            rsu_income=1e8, \
            rsu_ticker=GOOGLE_TICKER, \
            house_value_dollars=SAN_FRANCISCO_HOUSE_PRICE)

        gradient_apr = loanRiskProcessor.getGradientAprBucketed().quantize(TWO_PLACES)

        self.assertEqual(gradient_apr, Decimal(4.3).quantize(TWO_PLACES))

    def test_compute_differentials_contains_rsu_fields(self):
        loanRiskProcessor = LoanRiskProcessor(
            salary_income=GOOGLE_SALARY_INCOME, \
            rsu_income=GOOGLE_RSU_INCOME, \
            rsu_ticker=GOOGLE_TICKER, \
            house_value_dollars=SAN_FRANCISCO_HOUSE_PRICE)

        diff_output = loanRiskProcessor.computeDifferentials()

        self.assertEqual(diff_output['TraditionalRsu'], 0)
        self.assertEqual(diff_output['GradientRsu'], Decimal(116116.00).quantize(TWO_PLACES))

    def test_compute_differentials_contains_dti_fields(self):
        loanRiskProcessor = LoanRiskProcessor(
            salary_income=GOOGLE_SALARY_INCOME, \
            rsu_income=GOOGLE_RSU_INCOME, \
            rsu_ticker=GOOGLE_TICKER, \
            house_value_dollars=SAN_FRANCISCO_HOUSE_PRICE)

        diff_output = loanRiskProcessor.computeDifferentials()

        self.assertEqual(diff_output['TraditionalDti'], Decimal(0.38).quantize(TWO_PLACES))
        self.assertEqual(diff_output['GradientDti'], Decimal(0.25).quantize(TWO_PLACES))

    def test_compute_differentials_contains_interest_payment_totals(self):
        loanRiskProcessor = LoanRiskProcessor(
            salary_income=GOOGLE_SALARY_INCOME, \
            rsu_income=GOOGLE_RSU_INCOME, \
            rsu_ticker=GOOGLE_TICKER, \
            house_value_dollars=SAN_FRANCISCO_HOUSE_PRICE)

        diff_output = loanRiskProcessor.computeDifferentials()

        self.assertEqual(diff_output['TraditionalTotalInterestDollars'], Decimal(974438.99).quantize(TWO_PLACES))
        self.assertEqual(diff_output['GradientTotalInterestDollars'], Decimal(919823.50).quantize(TWO_PLACES))
        self.assertEqual(diff_output['InterestSavedDollars'], Decimal(54615.49).quantize(TWO_PLACES))

    def test_compute_differentials_contains_monthly_payment(self):
        loanRiskProcessor = LoanRiskProcessor(
            salary_income=GOOGLE_SALARY_INCOME, \
            rsu_income=GOOGLE_RSU_INCOME, \
            rsu_ticker=GOOGLE_TICKER, \
            house_value_dollars=SAN_FRANCISCO_HOUSE_PRICE)

        diff_output = loanRiskProcessor.computeDifferentials()

        self.assertEqual(diff_output['MonthlyPayment'], Decimal(5595.66).quantize(TWO_PLACES))
        self.assertEqual(diff_output['GradientMonthlyPayment'], Decimal(5443.95).quantize(TWO_PLACES))

    def test_compute_differentials_contains_max_house_values(self):
        loanRiskProcessor = LoanRiskProcessor(
            salary_income=GOOGLE_SALARY_INCOME, \
            rsu_income=GOOGLE_RSU_INCOME, \
            rsu_ticker=GOOGLE_TICKER, \
            house_value_dollars=SAN_FRANCISCO_HOUSE_PRICE)

        diff_output = loanRiskProcessor.computeDifferentials()

        self.assertEqual(diff_output['TraditionalMaxHouseValue'], Decimal(2016000))
        self.assertEqual(diff_output['GradientMaxHouseValue'], Decimal(2516000))


if __name__ == '__main__':
    unittest.main()
