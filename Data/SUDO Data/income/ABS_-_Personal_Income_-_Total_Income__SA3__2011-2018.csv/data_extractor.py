import csv
import json

csv_file = 'abs_personal_income_total_income_sa3_2011_2018-5856065762309795975.csv'
json_file = 'output.json'

data = {}

with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        sa3_name = row[' sa3_name']
        sa3_code = row[' sa3_code']
        median_income = row[' median_aud_2017_18']
        mean_income = row[' mean_aud_2017_18']
        
        if sa3_code not in data:
            data[sa3_code] = {'sa3_name': sa3_name, 'median_income': median_income, 'mean_income': mean_income}

with open(json_file, 'w') as file:
    json.dump(data, file, indent=2)

