from decimal import Decimal
# from ....gradient_loan import GradientLoan
from gradient_loan import GradientLoan

import unittest

TWO_PLACES = Decimal(10) ** -2


class GradientLoanTest(unittest.TestCase):

    # salary_income=1.5e6, rsu_income=1e6, rsu_ticker='GOOG', house_value_dollars=1e7

    def test_get_apr_returns_default_apr(self):
        loan = GradientLoan()
        self.assertEqual(loan.getApr().quantize(TWO_PLACES), \
                        Decimal(5.8).quantize(TWO_PLACES), "Should be 5.8%")

    def test_get_interest_returns_default_interest(self):
        loan = GradientLoan()
        self.assertEqual(loan.getInterest().quantize(TWO_PLACES), Decimal(.058).quantize(TWO_PLACES), "Should be .058")

    def test_get_apr_returns_correct_apr(self):
        loan = GradientLoan(interest_decimal=.045)
        self.assertEqual(loan.getApr().quantize(TWO_PLACES), Decimal(4.5).quantize(TWO_PLACES), "Should be 4.5%")

    def test_get_interest_returns_correct_interest(self):
        loan = GradientLoan(interest_decimal=.064)
        self.assertEqual(loan.getInterest().quantize(TWO_PLACES), Decimal(.064).quantize(TWO_PLACES), "Should be .064")


if __name__ == '__main__':
    unittest.main()
