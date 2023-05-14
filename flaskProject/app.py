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
total_sport_facility_suburb_db = couch['total_number_of_facility_suburb']
sport_facility_suburb_db = couch['']
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


@app.route('/get_sport_total/<param>', methods=['GET'])
def get_sport_total(param):
    # Mango Queries
    query = {
        "selector": {
            "Suburb": param
        }
    }
    # Execute the query
    results = []
    docs = total_sport_facility_suburb_db.find(query)
    for row in docs:
        results.append(row)
    # Return the results as JSON
    return {'data': results}


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
