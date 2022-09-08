import simplejson as json

from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)

'''
    Inputs:
    Output:
'''
@app.route('/getRateFromIncome', methods =['GET'])
@cross_origin()
def get_rates_from_income():
    # args = request.args
    # # Income comes from request and not firmographic characteristics
    # salary_income = args.get("salary_income", default=100000, type=int)
    # print("salary income from request: %f" % salary_income)
    # rsu_income = args.get("rsu_income", default=25000, type=int)
    # print("rsu income from request: %f" % rsu_income)
    # house_price = args.get("house_price", default=1e6, type=int)
    # print("house price: %f", house_price)
    # Use firmographic translator to get ticker

    # return json.dumps(loanRiskProcessor.computeDifferentials())
