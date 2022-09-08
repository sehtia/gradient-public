import simplejson as json

from firmographic_input_translator import FirmographicInputTranslator
from loan_risk_processor import LoanRiskProcessor
from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)

'''
    Inputs: salary_income, rsu_income, house_price
    Output: Mortgage differentials
'''
@app.route('/getRateFromIncome', methods =['GET'])
@cross_origin()
def get_rates_from_income():
    args = request.args
    # Income comes from request and not firmographic characteristics
    salary_income = args.get("salary_income", default=100000, type=int)
    print("salary income from request: %f" % salary_income)
    rsu_income = args.get("rsu_income", default=25000, type=int)
    print("rsu income from request: %f" % rsu_income)
    house_price = args.get("house_price", default=1e6, type=int)
    print("house price: %f", house_price)
    # Use firmographic translator to get ticker
    firmographic_translator = createFirmographicInputTranslator(args)
    ticker = firmographic_translator.getTicker()

    loanRiskProcessor = LoanRiskProcessor(salary_income, rsu_income, ticker, house_price)

    return json.dumps(loanRiskProcessor.computeDifferentials())


'''
    Inputs: company_name, job_title
    Output: salary_income, rsu_income
'''
@app.route('/getIncome', methods =['GET'])
@cross_origin()
def get_income():
    firmographic_translator = createFirmographicInputTranslator(request.args)
    return json.dumps(firmographic_translator.getAllIncome())

'''
    Inputs: city_name
    Output: house_value
'''
@app.route('/getCityHouseValue', methods=['GET'])
@cross_origin()
def get_house_value():
    firmographic_translator = createFirmographicInputTranslator(request.args)
    return json.dumps(firmographic_translator.getHouseValueAsDict())


'''
    Inputs: compan_name(default=Google), job_title(default=SoftwareEngineer), city_name(default=San Francisco)
    Ouput: Mortgage differentials
'''
@app.route('/getRate', methods =['GET'])
@cross_origin()
def get_rates():
    firmographic_translator = createFirmographicInputTranslator(request.args)
    salary_income = firmographic_translator.getSalaryIncome()
    rsu_income = firmographic_translator.getRsuIncome()
    house_value_dollars = firmographic_translator.getHouseValueDollars()
    ticker = firmographic_translator.getTicker()

    loanRiskProcessor = LoanRiskProcessor(salary_income, rsu_income, ticker, house_value_dollars)

    return json.dumps(loanRiskProcessor.computeDifferentials())


def createFirmographicInputTranslator(args):
    company_name = args.get("company_name", default="Google", type=str)
    job_title = args.get("job_title", default="Software Engineer", type=str)
    city_name = args.get("city_name", default="San Francisco", type=str)
    return FirmographicInputTranslator(company_name, job_title, city_name)
