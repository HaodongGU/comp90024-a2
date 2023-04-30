import csv
import json

csv_file = 'abs_data_by_region_pop_and_people_asgs_sa2_2011_2019-1575372530172239947.csv'
json_file = 'output.json'

data = {}

with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        sa2_name = row[' sa2_name_2016']
        sa2_code = row[' sa2_maincode_2016']
        median_age = row[' estmtd_rsdnt_ppltn_smmry_sttstcs_30_jne_mdn_age_prsns_yrs']
        
        if sa2_code not in data:
            data[sa2_code] = {'sa2_name': sa2_name, 'median_age': median_age}

with open(json_file, 'w') as file:
    json.dump(data, file, indent=2)

