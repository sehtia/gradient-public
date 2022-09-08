from decimal import Decimal

from buying_power_optimizer import BuyingPowerOptimizer

import unittest

TWO_PLACES = Decimal(10) ** -2

class BuyingPowerOptimizerTest(unittest.TestCase):

    def test_get_dti_house_value_is_correct(self):
        buying_power_optimizer = BuyingPowerOptimizer()

        house_value = buying_power_optimizer.getDtiHouseValue(Decimal(240000)).quantize(TWO_PLACES)

        self.assertEqual(house_value, 2016000)

    def test_get_dti_house_value_is_less_than_five_million(self):
        buying_power_optimizer = BuyingPowerOptimizer()

        house_value = buying_power_optimizer.getDtiHouseValue(Decimal(6e5)).quantize(TWO_PLACES)

        self.assertEqual(house_value, 5e6)

    def test_dti_house_values_difference_is_less_than_five_hundred_thousand(self):
        buying_power_optimizer = BuyingPowerOptimizer()
        salary_income = Decimal(150000) # 240K
        gradient_income = Decimal(350000) # 350K

        house_values = buying_power_optimizer.getDtiHouseValues(salary_income, gradient_income)

        house_diff = house_values[1] - house_values[0]
        self.assertLess(house_diff, 500001) # 500,001


    def test_get_dti_hosue_value_with_zero_income(self):
        buying_power_optimizer = BuyingPowerOptimizer()

        house_value = buying_power_optimizer.getDtiHouseValue(0)

        self.assertEqual(house_value, 0)

    def test_get_dti_hosue_value_with_negative_income(self):
        buying_power_optimizer = BuyingPowerOptimizer()

        house_value = buying_power_optimizer.getDtiHouseValue(0)

        self.assertEqual(house_value, 0)

if __name__ == '__main__':
    unittest.main()
