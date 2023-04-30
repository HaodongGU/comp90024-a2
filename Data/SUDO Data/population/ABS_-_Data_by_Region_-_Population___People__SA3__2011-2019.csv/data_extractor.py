import csv
import json

csv_file = 'abs_data_by_region_pop_and_people_asgs_sa3_2011_2019-2381592472532466826.csv'
json_file = 'output.json'

data = {}

with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        sa3_name = row[' sa3_name_2016']
        sa3_code = row[' sa3_code_2016']
        median_age = row[' estmtd_rsdnt_ppltn_smmry_sttstcs_30_jne_mdn_age_prsns_yrs']
        
        if sa3_code not in data:
            data[sa3_code] = {'sa3_name': sa3_name, 'median_age': median_age}

with open(json_file, 'w') as file:
    json.dump(data, file, indent=2)

