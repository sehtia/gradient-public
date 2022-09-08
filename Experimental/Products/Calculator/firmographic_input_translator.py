import numpy as np
import pandas as pd

'''
    Translate firmographic factors like company name and job title to income.
    Note: The values are hardcoded to be avoid I/O (reading csv file) on the
    backend for each request and be readable. Could move to JS, but more
    proficient in python.
    This needs to be optimized. Hacking rn okay.
'''

class FirmographicInputTranslator:

    DEFAULT_HOUSE_VALUE_DOLLARS = 1e6

    # New instructor instead of deleting old one to be backward compatible
    def __init__(self, company_name, job_title, city_name):
        self.city_name = city_name
        self.company_name = company_name
        self.job_title = job_title
        self.salary_data = pd.DataFrame(SALARY_INCOME, index=COMPANY_INDEX)
        self.rsu_data = pd.DataFrame(RSU_INCOME, index=COMPANY_INDEX)

    def getTicker(self):
        if self.company_name and self.company_name in COMPANY_TO_TICKER_MAP:
            return COMPANY_TO_TICKER_MAP[self.company_name]
        return 'GOOG'

    def getHouseValueDollars(self):
        if self.city_name and self.city_name in CITY_TO_HOUSE_PRICE:
            return CITY_TO_HOUSE_PRICE[self.city_name]
        return DEFAULT_HOUSE_VALUE_DOLLARS

    def getSalaryIncome(self):
        # Return .item() because numpy.int64 can't be converted to Decimal
        return self.salary_data.loc[self.company_name, self.job_title].item()

    def getRsuIncome(self):
        # Return .item() because numpy.int64 can't be converted to Decimal
        return self.rsu_data.loc[self.company_name][self.job_title].item()

    def getAllIncome(self):
        return {
            "salary_income": self.getSalaryIncome(),
            "rsu_income": self.getRsuIncome()
        }

    def getHouseValueAsDict(self):
        return { "house_value_dollars" : self.getHouseValueDollars() }

COMPANY_INDEX = ['Facebook', 'Amazon', 'Apple', 'Netflix', 'Google']

COMPANY_TO_TICKER_MAP = {
    'Facebook' : 'FB',
    'Apple' : 'AAPL',
    'Amazon' : 'AMZN',
    'Netflix' : 'NFLX',
    'Google' : 'GOOG'
}

#################### City Based Home Prices  ###################

CITY_TO_HOUSE_PRICE = {
    'Seattle': 829125,
    'New York': 1420124,
    'Denver': 575215,
    'Boston': 824300,
    'San Diego': 902124,
    'Los Angeles': 998052,
    'San Francisco': 1320522,
    'Miami': 535756
}

#################### SALARY INCOME MAPPING  ###################
SALARY_INCOME = {
    'Software Engineer': [
        219721, #Facebook
        175913, #Apple
        192730, #Amazon
        183205, #Netflix
        240083 #Google

     ],
    'Product Manager': [
        224518, #Facebook
        176959, #Apple
        212590, #Amazon
        182977, #Netflix
        252073 #Google
     ],
    'Data Scientist': [
        179060, #Facebook
        145484, #Apple
        169175, #Amazon
        154228, #Netflix
        202057 #Google
     ],
    'Product Designer': [
        189851, #Facebook
        150004, #Apple
        179601, #Amazon
        161820, #Netflix
        213008 #Google
     ],
    'Accountant': [
        178713, #Facebook
        138395, #Apple
        163883, #Amazon
        145744, #Netflix
        195083 #Google
     ],
    'Human Resources': [
        169374, #Facebook
        132364, #Apple
        160198, #Amazon
        144466, #Netflix
        193087 #Google
     ],
    'Marketing': [
        180860, #Facebook
        142180, #Apple
        167777, #Amazon
        146092, #Netflix
        204042 #Google
     ],
    'Program Manager': [
        173060, #Facebook
        138236, #Apple
        152173, #Amazon
        147237, #Netflix
        190011 #Google
     ],
    'Recruiter': [
        135379, #Facebook
        103185, #Apple
        122673, #Amazon
        113855, #Netflix
        147025 #Google
     ],
    'Sales': [
        217702, #Facebook
        169203, #Apple
        210546, #Amazon
        192674, #Netflix
        250035 #Google
     ]
}

#################### RSU INCOME MAPPING  ###################

RSU_INCOME = {
    'Software Engineer': [
        129721, #Facebook
        106685, #Apple
        122556, #Amazon
        107949, #Netflix
        144088 #Google
     ],
    'Product Manager': [
        110592, #Facebook
        88069, #Apple
        103410, #Amazon
        96609, #Netflix
        125078 #Google
     ],
    'Data Scientist': [
        53535, #Facebook
        43524, #Apple
        47115, #Amazon
        43150, #Netflix
        60098 #Google
     ],
    'Product Designer': [
        125690, #Facebook
        93484, #Apple
        109886, #Amazon
        95912, #Netflix
        135051 #Google
     ],
    'Accountant': [
        79112, #Facebook
        61797, #Apple
        72493, #Amazon
        60561, #Netflix
        85059 #Google
     ],
    'Human Resources': [
        15107, #Facebook
        12134, #Apple
        14219, #Amazon
        12551, #Netflix
        17076 #Google
     ],
    'Marketing': [
        56610, #Facebook
        46916, #Apple
        52089, #Amazon
        48033, #Netflix
        65033 #Google
     ],
    'Program Manager': [
        39716, #Facebook
        30352, #Apple
        37993, #Amazon
        32227, #Netflix
        45092 #Google
     ],
    'Recruiter': [
        82141, #Facebook
        61856, #Apple
        71194, #Amazon
        66381, #Netflix
        90009 #Google
     ],
    'Sales': [
        46416, #Facebook
        35398, #Apple
        42216, #Amazon
        37964, #Netflix
        50039 #Google
     ]
}
