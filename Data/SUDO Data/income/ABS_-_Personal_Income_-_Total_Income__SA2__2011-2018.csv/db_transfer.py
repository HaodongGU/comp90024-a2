import couchdb
import json

# Connect to CouchDB
couch = couchdb.Server('http://admin:password@172.26.135.165:5984/')
db_name = 'incomesa2'
if db_name in couch:
    db = couch[db_name]
else:
    db = couch.create(db_name)

# Read data from JSON file
with open('output.json') as f:
    data = json.load(f)

# Write data to CouchDB
for doc_id, doc_data in data.items():
    doc = {'_id': doc_id, 'sa2_name': doc_data['sa2_name'], 'median_income': doc_data['median_income'], 'mean_income': doc_data['mean_income']}
    db.save(doc)
