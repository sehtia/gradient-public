<script>
// Check if company-name was updated
document.getElementById('company-name').addEventListener('change', function() {
    console.log('You selected: ', this.value);
    job_title = document.getElementById("job-title").value;
    if (job_title) {
        console.log("job title:", job_title);
        updateIncome(this.value, job_title);
    } else {
        console.log("Job title has not been set")
    }
});

// Check if job-title was updated
document.getElementById('job-title').addEventListener('change', function() {
    console.log('You selected: ', this.value);
    company_name = document.getElementById("company-name").value;
    if (company_name) {
        console.log("company_name: ", company_name);
        updateIncome(company_name, this.value);
    } else {
        console.log("Company name has not been set")
    }
});

// Check if city-name was updated
document.getElementById('city-name').addEventListener('change', function() {
    if (this.value) {
        updateHousePrice(this.value);
    } else {
        console.log("City name has not been set")
    }
});

// Income is based on company_nam and job_title
const updateIncome = async (company_name, job_title) => {
    try {
        // TODO: Format url instead
        const data = await fetch(
            `https://gradient.pythonanywhere.com/getIncome?company_name=${company_name}&job_title=${job_title}`
        );
        const json = await data.json();
        document.getElementById('salary-income').value = json.salary_income.toLocaleString();
        document.getElementById('rsu-income').value = json.rsu_income.toLocaleString();
        // Dispatch event to update rates when inputs selected
        document.getElementById('salary-income').dispatchEvent(new Event('keyup'))
        console.log(json);
    } catch (err) {
        console.error(`Error getting income: ${err}`);
    }
};

const updateHousePrice = async (city_name) => {
    try {
        const data = await fetch(
            `https://gradient.pythonanywhere.com/getCityHouseValue?city_name=${city_name}`
        );
        const json = await data.json();
        document.getElementById('house-price').value = json.house_value_dollars.toLocaleString();
        document.getElementById('house-price').dispatchEvent(new Event('keyup'));
    } catch (err) {
        console.error(`Error getting income: ${err}`);
    }
};

document.getElementById('salary-income').addEventListener('keyup', function() {
    // Add commas when user manually changes input.
    // this.value = this.value.toLocaleString();
    safeUpdateRatesAndStuff();
});

document.getElementById('rsu-income').addEventListener('keyup', function() {
    safeUpdateRatesAndStuff();
});

document.getElementById('house-price').addEventListener('keyup', function() {
    safeUpdateRatesAndStuff();
});

function safeUpdateRatesAndStuff() {
    console.log("getting APRs");
    salary = document.getElementById('salary-income').value;
    console.log("salary is: ", salary);
    console.log("type of: ", typeof salary);
    salary = parseStringFieldToNumber(salary);
    if (!salary) {
        console.log("salary-income not set");
        return;
    }
    rsu = document.getElementById('rsu-income').value;
    rsu = parseStringFieldToNumber(rsu);
    if (!rsu) {
        console.log("rsu-income not set");
        return;
    }
    house_price = document.getElementById('house-price');
    if (house_price && house_price.value) {
        //house_price = house_price.value
        house_price = parseStringFieldToNumber(house_price.value);
    } else {
        console.log("house price not set");
        return;
    }

    company_name = document.getElementById('company-name').value;
    updateRatesAndStuff(company_name, salary, rsu, house_price);
}

// Parses a string field with commas (used to represent dollar amounts).
function parseStringFieldToNumber(field) {
    console.log("field: ", field);
    console.log("type of field: ", typeof field);
    return parseFloat(field.replace(/,/g, ''));
    // return parseFloat(field.replaceAll(',', ''));
}

/**
  document.getElementById('get-apr').addEventListener("click", function() {
  	console.log("getting APRs");
    salary = document.getElementById('salary-income').value;
    rsu = document.getElementById('rsu-income').value;
    company_name = document.getElementById('company-name').value;
    if (!salary) {
    	console.log("salary-income not set");
    	return;
    }
    if (!rsu) {
    	console.log("rsu-income not set");
    	return;
    }
    updateRatesAndStuff(company_name, salary, rsu);
  });

  */

let formatter = Intl.NumberFormat('en', {
    notation: 'compact'
});

// Rates are based on
// Can we remove company name now?
const updateRatesAndStuff = async (company_name, salary, rsu, house_price) => {
    try {
        const data = await fetch(
            `https://gradient.pythonanywhere.com/getRateFromIncome?company_name=${company_name}&salary_income=${salary}&rsu_income=${rsu}&house_price=${house_price}`
        );
        const json = await data.json();
        document.getElementById('gradient-apr').innerHTML = json.GradientApr + "%";
        document.getElementById('traditional-apr').innerHTML = json.TraditionalApr + "%";
        // TODO(): Format the strings properly
        document.getElementById('gradient-rsu').innerHTML =
            "Gradient: $" + json.GradientRsu.toLocaleString();
        // DTIs
        traditional_dti = Math.round(json.TraditionalDti * 100);
        document.getElementById('traditional-dti').innerHTML =
            "Traditional: " + traditional_dti + "%";
        gradient_dti = Math.round(json.GradientDti * 100);
        document.getElementById('gradient-dti').innerHTML =
            "Gradient: " + gradient_dti + "%";
        // Interest Payments
        //document.getElementById('gradient-monthly').innerHTML =
        //	"$" + Math.round(json.GradientMonthlyPayment).toLocaleString();
        // document.getElementById('traditional-monthly').innerHTML =
        //	"$" + Math.round(json.MonthlyPayment).toLocaleString();
        document.getElementById('interest-savings').innerHTML =
            "$" + Math.round(json.InterestSavedDollars).toLocaleString();
        // Purchasing power
        document.getElementById('gradient-loan-size').innerHTML =
            "$" + formatter.format(json.GradientMaxLoanValue);
        document.getElementById('traditional-loan-size').innerHTML =
            "$" + formatter.format(json.TraditionalMaxLoanValue);
        purchase_power = json.GradientMaxLoanValue - json.TraditionalMaxLoanValue;
        document.getElementById('borrowing-power').innerHTML =
            "$" + formatter.format(purchase_power)
    } catch (err) {
        console.error(`Error getting Gradient rates: ${err}`);
    }
};

 </script>
