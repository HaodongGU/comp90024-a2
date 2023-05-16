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
employment_db = couch['employment']
income_db = couch['income']
population_db = couch['']
age_db = couch['']
twitter_db = couch['twitter']
mastodon_db = couch['']


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


#######################################################################################################################
#       scenario 1 The top5 with the most sports facilities and the bottom five
#######################################################################################################################

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
sport_total_design_doc_id = "_design/total_facilities_by_suburb_view"
if sport_total_design_doc_id in sport_facility_suburb_db:
    print("get_sport_total_map_func Design document already exists.")
else:
    print("get_sport_total_map_func Design document does not exist. Creating it now.")
    # Create the view
    sport_facility_suburb_db.save({
        "_id": sport_total_design_doc_id,
        "views": {
            "by_suburb": {
                "map": get_sport_total_map_func,
                "reduce": get_sport_total_reduce_func
            }
        }
    })


# Get top5 with the most sports facilities and the bottom five suburb
@app.route('/get_top_bot_sport', methods=['GET'])
def get_top_bot_sport():
    result = sport_facility_suburb_db.view('total_facilities_by_suburb_view/by_suburb', group=True)

    # Convert the result to a list of dictionaries
    suburbs = [{'Suburb': row.key, 'total_facilities': row.value} for row in result]

    # Sort the list of dictionaries by total_facilities
    sorted_suburbs = sorted(suburbs, key=lambda k: k['total_facilities'])

    # Get the top 5 and bottom 5 suburbs
    top_suburbs = sorted_suburbs[-5:]
    bottom_suburbs = sorted_suburbs[:5]

    return {'Top 5 Suburbs': top_suburbs, 'Bottom 5 Suburbs': bottom_suburbs}


@app.route('/get_sport_total/<param>', methods=['GET'])
def get_sport_total(param):
    # Get the total facilities for a suburb
    result = sport_facility_suburb_db.view('total_facilities_by_suburb_view/by_suburb', key=param)
    total = 0
    for row in result:
        total = row.value
    # Return the result as JSON
    return {'Suburb': param, 'total_facilities': total}


# Get the data of a specific suburb， param is suburb name
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


#######################################################################################################################
#       scenario 2 The top5 employ rate and unemployed rate SA4
#       DJSB Labour Market Data - Population by Labour Force Status SA4 2018
#######################################################################################################################
# Map function
get_fulltime_rate_func = '''function(doc) {
    if (doc.sa4_name11 && doc.employed_fulltime && doc.employed_parttime && doc.not_in_labour_force && doc.unemployed_total) {
        var total = doc.employed_parttime + doc.employed_fulltime + doc.unemployed_total;
        var fulltime_rate = doc.employed_fulltime / total;
        emit(doc.sa4_name11, fulltime_rate);
    }
}
'''
get_unemployed_rate_func = '''function(doc) {
    if (doc.sa4_name11 && doc.employed_fulltime && doc.employed_parttime && doc.not_in_labour_force && doc.unemployed_total) {
        var total = doc.employed_parttime + doc.employed_fulltime + doc.unemployed_total;
        var unemployment_rate = doc.unemployed_total / total;
        emit(doc.sa4_name11, unemployment_rate);
    }
}
'''

# Create the view
# Check if the design document already exists
fulltime_rate_id = "_design/get_fulltime_rate_view"
if fulltime_rate_id in employment_db:
    print("fulltime_rate_id Design document already exists.")
    # Get the existing design document
    # design_doc = employment_db[fulltime_rate_id]
    # # Update the view
    # design_doc['views']['by_sa4_name11']['map'] = get_fulltime_rate_func
    # # Save the updated design document back to the database
    # employment_db.save(design_doc)
else:
    print("fulltime_rate_id Design document does not exist. Creating it now.")
    # Create the view
    employment_db.save({
        "_id": fulltime_rate_id,
        "views": {
            "by_sa4_name11": {
                "map": get_fulltime_rate_func,
            }
        }
    })
get_unemployed_rate_id = "_design/get_unemployed_rate_view"
if get_unemployed_rate_id in employment_db:
    print("fulltime_rate_id Design document already exists.")
    # Get the existing design document
    # design_doc = employment_db[get_unemployed_rate_id]
    # # Update the view
    # design_doc['views']['by_sa4_name11']['map'] = get_unemployed_rate_func
    # # Save the updated design document back to the database
    # employment_db.save(design_doc)
else:
    print("fulltime_rate_id Design document does not exist. Creating it now.")
    # Create the view
    employment_db.save({
        "_id": get_unemployed_rate_id,
        "views": {
            "by_sa4_name11": {
                "map": get_unemployed_rate_func,
            }
        }
    })


@app.route('/employment_top_top', methods=['GET'])
def employment_top_bot():
    # Fulltime rate
    fulltime_rate_view = employment_db.view('get_fulltime_rate_view/by_sa4_name11')
    fulltime_rate_results = [dict(sa4_name11=row.key, fulltime_rate=row.value) for row in fulltime_rate_view]
    fulltime_rate_results.sort(key=lambda x: x['fulltime_rate'], reverse=True)
    top_5_fulltime_rate = fulltime_rate_results[:5]

    # Unemployment rate
    unemployment_rate_view = employment_db.view('get_unemployed_rate_view/by_sa4_name11')
    unemployment_rate_results = [dict(sa4_name11=row.key, unemployment_rate=row.value) for row in
                                 unemployment_rate_view]
    unemployment_rate_results.sort(key=lambda x: x['unemployment_rate'], reverse=True)
    top_5_unemployment_rate = unemployment_rate_results[:5]

    # Return the results as JSON
    return {
        'top_5_fulltime_rate': top_5_fulltime_rate,
        'top_5_unemployment_rate': top_5_unemployment_rate,
    }


#######################################################################################################################
#       scenario 3 The top5 median income and bot5 sa2_name
#
#######################################################################################################################
# CouchDB defaults to sorting in ascending key order
income_func = '''function(doc) {
    if (doc.sa2_name && doc.median_income != null) {
        var income = parseFloat(doc.median_income);
        if (!isNaN(income)) {
            emit(income, doc.sa2_name);
        }
    }
}'''

# Create the view
income_doc_id = "_design/income_by_sa2_name_view"
if income_doc_id in income_db:
    print("income_func Design document already exists. Updating it now.")
    # Get the existing design document
    # design_doc = income_db[income_doc_id]
    # # Update the view
    # design_doc['views']['by_sa2_name'] = {"map": income_func}
    # # Save the updated design document back to the database
    # income_db.save(design_doc)
else:
    print("income_func Design document does not exist. Creating it now.")
    # Create the view
    income_db.save({
        "_id": income_doc_id,
        "views": {
            "by_sa2_name": {
                "map": income_func
            }
        }
    })


@app.route('/income_db_top_bot', methods=['GET'])
def income_db_top_bot():
    # Query the view
    results = income_db.view('income_by_sa2_name_view/by_sa2_name')
    sorted_results = [dict(sa2_name=row.value, median_income=row.key) for row in results]
    # Get top 5 and bottom 5
    top_5 = sorted_results[-5:]
    bottom_5 = sorted_results[:5]
    # Return the results as JSON
    return {'Top 5': top_5, 'Bottom 5': bottom_5}


#######################################################################################################################
#       scenario 4 The top5 median income and bot5 sa2_name
#
#######################################################################################################################

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


# Map function
get_twitter_total_map_func = '''function(doc) {
    if (doc.Place && doc["Sentiment Score"]) {
        var total = parseFloat(doc["Sentiment Score"]);
        emit(doc.Place, total);
    }
}'''

# Reduce function
get_twitter_total_reduce_func = '''function(keys, values) {
    var total = sum(values);
    var count = values.length;
    return {total: total, count: count};
}'''

# Create the view
# Check if the design document already exists
twitter_design_doc_id = "_design/total_senti_by_suburb_view"
if twitter_design_doc_id in twitter_db:
    print("Design document already exists. Updating it now.")
    design_doc = twitter_db[twitter_design_doc_id]

    # Update the view
    design_doc['views'] = {
        "by_suburb_sentiment": {
            "map": get_twitter_total_map_func,
            "reduce": get_twitter_total_reduce_func
        }
    }

    # Save the updated design document back to the database
    twitter_db.save(design_doc)

else:
    print("Design document does not exist. Creating it now.")
    # Create the view
    twitter_db.save({
        "_id": twitter_design_doc_id,
        "views": {
            "by_suburb_sentiment": {
                "map": get_twitter_total_map_func,
                "reduce": get_twitter_total_reduce_func
            }
        }
    })


@app.route('/twitter_db_get/<param>', methods=['GET'])
def twitter_db_get(param):
    # Get the total facilities for a suburb
    result = twitter_db.view('total_senti_by_suburb_view/by_suburb_sentiment', key=str(param))

    total = 0
    count = 0
    for row in result:
        total = row.value['total']
        count = row.value['count']

    # Calculate the average
    # avg_senti = total / count if count != 0 else 0

    # Return the result as JSON
    # return {'Place': param, 'total_senti': total, "avg_senti": avg_senti}
    return {'Place': param, 'total_senti': total, "avg_senti": count}


@app.route('/twitter_dbtry_get/<param>', methods=['GET'])
def twitter_dbtry_get(param):
    # Get the total facilities for a suburb
    result = twitter_db.view('tweeter/new-view', key=str(param))
    print(result)
    for i in result:
        tmp = i.value["count"]

    return {"total": tmp}
    # Calculate the average
    # avg_senti = total / count if count != 0 else 0

    # Return the result as JSON
    # return {'Place': param, 'total_senti': total, "avg_senti": avg_senti}
    # return {'Place': param, 'total_senti': total, "avg_senti": count}


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
