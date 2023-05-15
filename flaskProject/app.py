from flask import Flask, render_template
from flask_restful import Api, Resource
# from flask_cors import CORS

import couchdb

app = Flask(__name__)

# authentication
admin = 'admin'
password = 'admin'
url = f'http://{admin}:{password}@172.26.135.221:5984/'

# get couchdb instance
couch = couchdb.Server(url)

# indicate the db name
# total_sport_facility_suburb_db = couch['total_number_of_facility_suburb']
sport_facility_suburb_db = couch['sports_facility_suburb']
internet_db = couch['']
public_transport_db = couch['']
employment_db = couch['']
income_db = couch['']
population_db = couch['']
age_db = couch['']
twitter_db = couch['']
mastodon_db = couch['']


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


# Get the data of a specific suburb
@app.route('/get_sport_specific/<param>', methods=['GET'])
def get_sport_specific(param):
    # Mango Queries
    query = {
        "selector": {
            "Suburb": param
        }
    }
    # Execute the query
    results = []
    docs = sport_facility_suburb_db.find(query)
    for row in docs:
        results.append(row)
    # Return the results as JSON
    return {'data': results}


# Map function
get_sport_total_map_func = '''function(doc) {
    if (doc.Suburb) {
        var total = 0;
        for (var facility in doc) {
            if (facility != "Suburb" && facility != "_id" && facility != "_rev" && typeof doc[facility] == "number") {
                total += doc[facility];
            }
        }
        emit(doc.Suburb, total);
    }
}'''

# Reduce function
get_sport_total_reduce_func = '_sum'

# Create the view
# Check if the design document already exists
design_doc_id = "_design/total_facilities_by_suburb_view"
if design_doc_id in sport_facility_suburb_db:
    print("Design document already exists.")
else:
    print("Design document does not exist. Creating it now.")
    # Create the view
    sport_facility_suburb_db.save({
        "_id": design_doc_id,
        "views": {
            "by_suburb": {
                "map": get_sport_total_map_func,
                "reduce": get_sport_total_reduce_func
            }
        }
    })

@app.route('/get_sport_total/<param>', methods=['GET'])
def get_sport_total(param):
    # Get the total facilities for a suburb
    result = sport_facility_suburb_db.view('total_facilities_by_suburb_view/by_suburb', key=param)
    total = 0
    for row in result:
        total = row.value
    # Return the result as JSON
    return {'Suburb': param, 'total_facilities': total}


@app.route('/internet_db/<param>', methods=['GET'])
def internet_db(param):
    # Mango Queries
    query = {
        "selector": {
            "Suburb": param
        }
    }
    # Execute the query
    results = []
    docs = internet_db.find(query)
    for row in docs:
        results.append(row)
    # Return the results as JSON
    return {'data': results}


@app.route('/public_transport_db/<param>', methods=['GET'])
def public_transport_db(param):
    # Mango Queries
    query = {
        "selector": {
            "Suburb": param
        }
    }
    # Execute the query
    results = []
    docs = public_transport_db.find(query)
    for row in docs:
        results.append(row)
    # Return the results as JSON
    return {'data': results}


@app.route('/employment_db/<param>', methods=['GET'])
def employment_db(param):
    # Mango Queries
    query = {
        "selector": {
            "Suburb": param
        }
    }
    # Execute the query
    results = []
    docs = employment_db.find(query)
    for row in docs:
        results.append(row)
    # Return the results as JSON
    return {'data': results}


@app.route('/income_db/<param>', methods=['GET'])
def income_db(param):
    # Mango Queries
    query = {
        "selector": {
            "Suburb": param
        }
    }
    # Execute the query
    results = []
    docs = income_db.find(query)
    for row in docs:
        results.append(row)
    # Return the results as JSON
    return {'data': results}


@app.route('/population_db/<param>', methods=['GET'])
def population_db(param):
    # Mango Queries
    query = {
        "selector": {
            "Suburb": param
        }
    }
    # Execute the query
    results = []
    docs = population_db.find(query)
    for row in docs:
        results.append(row)
    # Return the results as JSON
    return {'data': results}


@app.route('/age_db/<param>', methods=['GET'])
def age_db(param):
    # Mango Queries
    query = {
        "selector": {
            "Suburb": param
        }
    }
    # Execute the query
    results = []
    docs = age_db.find(query)
    for row in docs:
        results.append(row)
    # Return the results as JSON
    return {'data': results}


@app.route('/twitter_db/<param>', methods=['GET'])
def twitter_db(param):
    # Mango Queries
    query = {
        "selector": {
            "Suburb": param
        }
    }
    # Execute the query
    results = []
    docs = twitter_db.find(query)
    for row in docs:
        results.append(row)
    # Return the results as JSON
    return {'data': results}


@app.route('/mastodon_db/<param>', methods=['GET'])
def mastodon_db(param):
    # Mango Queries
    query = {
        "selector": {
            "Suburb": param
        }
    }
    # Execute the query
    results = []
    docs = mastodon_db.find(query)
    for row in docs:
        results.append(row)
    # Return the results as JSON
    return {'data': results}


if __name__ == '__main__':
    app.run(debug=True)
