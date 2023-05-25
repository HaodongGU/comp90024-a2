import csv
import json
import couchdb

csv_file = '../CouchDB_mrc/abs_personal_income_total_income_sa2_2011_2018-5100138388407574581.csv'
json_file = 'output.json'

data = {}

with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        sa2_name = row[' sa2_name']
        sa2_code = row[' sa2_code']
        median_income = row[' median_aud_2017_18']
        mean_income = row[' mean_aud_2017_18']

        if sa2_code not in data:
            data[sa2_code] = {'sa2_name': sa2_name, 'median_income': median_income, 'mean_income': mean_income}
couch = couchdb.Server('https://admin:password@localhost:5984')
print(1)
db_name = 'income_suburb'
print(2)
# if db_name not in couch:
db = couch.create(db_name)
# else:
#     db = couch[db_name]
print(3)
for i in data:
    db.save(data[i])

# with open(json_file, 'w') as file:
#     json.dump(data, file, indent=2)