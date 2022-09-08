## Local Run

1. In order to run locally, cd into the Calculator directory and run:
  1. `export FLASK_APP=calculator_service.py`
  1. `flask run`
1. In a separate terminal, also in the Calculator/, run the following command
to hit the getRates endpoint:

`curl "localhost:5000/getRate?company_name=Facebook&job_title=Software%20Engineer"`

1. Hitting the getIncome endpoint:

`curl "localhost:5000/getIncome?company_name=Facebook&job_title=Software%20Engineer"`

1. Hitting the getRateFromIncome endpoint:

`curl "localhost:5000/getRateFromIncome?company_name=Facebook&salary_income=200000&rsu_income=50000&city_name=Seattle"`

1. Shout out to the boiz


## Architecture

TODO(): Explain how pieces talk to each other
