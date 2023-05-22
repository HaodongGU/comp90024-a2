from flask import Flask, render_template, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
import numpy as np
from datetime import datetime

import couchdb

app = Flask(__name__)
CORS(app)

# authentication
admin = 'admin'
password = 'admin'
url = f'http://{admin}:{password}@172.26.135.221:5984/'

# get couchdb instance
couch = couchdb.Server(url)

# indicate the db name
# total_sport_facility_suburb_db = couch['total_number_of_facility_suburb']
sport_facility_suburb_db = couch['sports_facility_suburb']
public_transport_db = couch['transport']
employment_db = couch['employment']
income_db = couch['income']
population_db = couch['population_sa2_data']
age_db = couch['median_age_sa2_data']
crime_db = couch['crime_data']


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/hello_world_json')
def hello_world_json():  # put application's code here
    data = {
        'name': 'Changwen Li',
        'greeting': 'Hello World',
        'city': 'Melb'
    }
    return jsonify(data)


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
@app.route('/sports_top_bot', methods=['GET'])
def sport_top_bot():
    result = sport_facility_suburb_db.view('total_facilities_by_suburb_view/by_suburb', group=True)

    # Convert the result to a list of dictionaries
    suburbs = [{'name': row.key, 'value': row.value} for row in result]

    # Sort the list of dictionaries by total_facilities
    sorted_suburbs = sorted(suburbs, key=lambda k: k['value'])

    # Get the top 5 and bottom 5 suburbs
    top_suburbs = sorted_suburbs[-25:]
    bottom_suburbs = sorted_suburbs[:25]
    meta_sport = {
        'name': 'sa2 name',
        'value': 'sports facilities'
    }
    return {'meta': meta_sport, 'top data': top_suburbs, 'bottom data': bottom_suburbs}


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
#       scenario 2 The top5 employ rate and unemployed rate SA4      sa2？？？？？？？？？？？？
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


@app.route('/employment_top_bot', methods=['GET'])
def employment_top_bot():
    # Fulltime rate
    fulltime_rate_view = employment_db.view('get_fulltime_rate_view/by_sa4_name11')
    fulltime_rate_results = [dict(name=row.key, value=row.value) for row in fulltime_rate_view]
    fulltime_rate_results.sort(key=lambda x: x["value"], reverse=True)
    top_10_fulltime_rate = fulltime_rate_results[:10]

    # Unemployment rate
    unemployment_rate_view = employment_db.view('get_unemployed_rate_view/by_sa4_name11')
    unemployment_rate_results = [dict(name=row.key, value=row.value) for row in
                                 unemployment_rate_view]
    unemployment_rate_results.sort(key=lambda x: x["value"], reverse=True)
    top_10_unemployment_rate = unemployment_rate_results[:10]

    meta_emp = {
        'name': 'sa4 name',
        'value': 'emp unemp rate'
    }

    return {
        'meta': meta_emp,
        'top data': top_10_fulltime_rate,
        'bottom data': top_10_unemployment_rate,
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


# Please use this request as a template.
@app.route('/income_top_bot', methods=['GET'])
def income_top_bot():
    # lcw: create meta data, storing discription of data attributes
    meta_income = {
        'name': 'sa2 name',
        'value': 'median income (AUD/year)'
    }
    # Query the view
    results = income_db.view('income_by_sa2_name_view/by_sa2_name')
    sorted_results = [dict(name=row.value, value=row.key) for row in results]
    # Get top 5 and bottom 5
    top_5 = sorted_results[-25:]
    bottom_5 = sorted_results[:25]
    # Return the results as JSON
    return {'meta': meta_income, 'top data': top_5, 'bottom data': bottom_5}


#######################################################################################################################
#       scenario 4 The top5 crime and bot 5 crime lga_name11 and lga_code11
# This dataset presents the footprint of the number of criminal incidents by principal offence recorded on the Victoria
# Police Law Enforcement Assistance Program (LEAP).
#       VIC CSA - Crime Statistics - Criminal Incidents by Principal Offence (LGA) 2010-2019
#######################################################################################################################

# there is a space before each features.........
crime_func = '''function(doc) {
    if (doc[" lga_name11"] && doc[" lga_code11"]) {
        var total = 0;
        if (doc[" total_division_a_offences"] != "null") {
            total += parseInt(doc[" total_division_a_offences"]);
        }
        if (doc[" total_division_b_offences"] != "null") {
            total += parseInt(doc[" total_division_b_offences"]);
        }
        if (doc[" total_division_c_offences"] != "null") {
            total += parseInt(doc[" total_division_c_offences"]);
        }
        if (doc[" total_division_d_offences"] != "null") {
            total += parseInt(doc[" total_division_d_offences"]);
        }
        if (doc[" total_division_e_offences"] != "null") {
            total += parseInt(doc[" total_division_e_offences"]);
        }
        if (doc[" total_division_f_offences"] != "null") {
            total += parseInt(doc[" total_division_f_offences"]);
        }
        emit(doc[" lga_name11"], {"total": total, "lga_code11": doc[" lga_code11"]});
    }
}'''

# Create the view
crime_id = "_design/crime_func_view"
if crime_id in crime_db:
    print("crime_func_view Design document already exists. Updating it now.")
    # # Get the existing design document
    # design_doc = crime_db[crime_id]
    # # Update the view
    # design_doc['views']['by_ga_name11'] = {"map": crime_func}
    # # Save the updated design document back to the database
    # crime_db.save(design_doc)
else:
    print("crime_func_view Design document does not exist. Creating it now.")
    # Create the view
    crime_db.save({
        "_id": crime_id,
        "views": {
            "by_ga_name11": {
                "map": crime_func
            }
        }
    })


@app.route('/crime_top_bot/', methods=['GET'])
def crime_top_bot():
    # Get crime total
    crime_view = crime_db.view('crime_func_view/by_ga_name11')
    crime_results = [dict(name=row.key, value=row.value["total"]) for row in
                     crime_view]
    crime_results.sort(key=lambda x: x['value'])
    top_5_crime = crime_results[-50:]
    bottom_5_crime = crime_results[:50]
    meta_cri = {
        'name': 'lga name',
        'value': 'crime counts'
    }
    # Return the results as JSON
    return {"meta": meta_cri, 'top data': top_5_crime, 'bottom data': bottom_5_crime}


#######################################################################################################################
#       scenario 5 The top5 and bot 5 median age sa2_name
#
#######################################################################################################################
# Define a map function that emits median_age and sa2_name
age_view_map_func = '''function(doc) {
    if (doc.sa2_name && doc.median_age) {
        emit(parseFloat(doc.median_age), doc.sa2_name);
    }
}'''

# Create the view
age_view_id = "_design/age_view"
if age_view_id in age_db:
    print("age_view_id Design document already exists. Updating it now.")
    # # Get the existing design document
    # design_doc = crime_db[crime_id]
    # # Update the view
    # design_doc['views']['by_ga_name11'] = {"map": crime_func}
    # # Save the updated design document back to the database
    # crime_db.save(design_doc)
else:
    print("age_view_id Design document does not exist. Creating it now.")
    # Create the view
    age_db.save({
        "_id": age_view_id,
        "views": {
            "by_median_age": {
                "map": age_view_map_func
            }
        }
    })


@app.route('/age_top_bot/', methods=['GET'])
def age_top_bot():
    # lcw: create meta data, storing discription of data attributes
    meta = {
        'name': 'sa2 name',
        'value': 'median age (years)'
    }
    # Get ages
    age_view = age_db.view('age_view/by_median_age')
    age_results = [dict(name=row.value, value=row.key) for row in age_view]
    # age_results.sort(key=lambda x: x['value'], reverse=True)
    # top_5_age = age_results[:10]
    # bottom_5_age = age_results[-10:]
    age_results.sort(key=lambda x: x['value'])
    top_5_age = age_results[-25:]
    bottom_5_age = age_results[:25]

    # Return the results as JSON
    return {'meta': meta, 'top data': top_5_age, 'bottom data': bottom_5_age}


#######################################################################################################################
#       scenario 6 The top5 and bot 5 Composite Accessibility Index
# This dataset presents the Spatial Network Analysis for Multimodal Urban Transport Systems (SNAMUTS) indicators by
# activity node locations for the year of 2016.
#
# Composite Accessibility Index: This index can be a good choice for accessibility, as it usually takes into account the
# time or distance to various facilities such as schools, hospitals, shopping centers, and so on.
#######################################################################################################################
composite_index_view_map_func = '''function(doc) {
    if (doc.coordinates && doc.composite_index) {
        emit(parseFloat(doc.composite_index), doc.coordinates);
    }
}'''

# Create the view
public_transport_view_id = "_design/composite_index_view"
if public_transport_view_id in public_transport_db:
    print("composite_index_view Design document already exists. Updating it now.")
else:
    print("composite_index_view Design document does not exist. Creating it now.")
    # Create the view
    public_transport_db.save({
        "_id": public_transport_view_id,
        "views": {
            "by_composite_index": {
                "map": composite_index_view_map_func
            }
        }
    })


@app.route('/transport_top_bot/', methods=['GET'])
def transport_top_bot():
    # Get public transport data
    public_transport_view = public_transport_db.view('composite_index_view/by_composite_index')
    public_transport_dict = {}
    for row in public_transport_view:
        if row.value in public_transport_dict:
            public_transport_dict[row.value].append(row.key)
        else:
            public_transport_dict[row.value] = [row.key]

    # Calculate average composite_index for each coordinates
    avg_composite_index_dict = {coordinates: sum(values) / len(values) for coordinates, values in
                                public_transport_dict.items()}

    # Sort by composite_index and get top 5 and bottom 5
    sorted_composite_index_list = sorted(avg_composite_index_dict.items(), key=lambda x: x[1])

    # Convert top and bottom lists to desired format
    top_5_public_transport = [{"name": location, "value": index} for location, index in
                              sorted_composite_index_list[-25:]]
    bottom_5_public_transport = [{"name": location, "value": index} for location, index in
                                 sorted_composite_index_list[:25]]

    meta = {
        'name': 'station',
        'value': 'CAI transport'
    }
    # Return the results as JSON
    return {"meta": meta, 'top data': top_5_public_transport, 'bottom data': bottom_5_public_transport}


#######################################################################################################################
#       scenario 7 The top5 and bot 5 population density   sa2name sa2density
#
#######################################################################################################################
get_top_density_func = """
function (doc) {
  if (parseFloat(doc[" population_density_as_at_30_june_population_density_personskm2"]) && doc[" sa2_name_2016"] && doc[" sa2_maincode_2016"]) {
    emit(parseFloat(doc[" population_density_as_at_30_june_population_density_personskm2"]), {sa2_name_2016: doc[" sa2_name_2016"], sa2_maincode_2016: doc[" sa2_maincode_2016"]});
  }
}
"""

# Create the view
top_density_view_id = "_design/top_density_view"
if top_density_view_id in population_db:
    print("top_density_view Design document already exists. Updating it now.")
    population_db.delete(population_db[top_density_view_id])
    # design_doc = population_db[top_density_view_id]
    ##
    # # Update the view
    # design_doc['views']['by_density'] = {"map": get_top_density_func}
    # # Save the updated design document back to the database
    # population_db.save(design_doc)

print("top_density_view Design document does not exist. Creating it now.")
population_db.save({
    "_id": top_density_view_id,
    "views": {
        "by_density": {
            "map": get_top_density_func
        }
    }
})


@app.route('/population_top_bot', methods=['GET'])
def population_top_bot():
    # Fetch the view
    view = population_db.view("top_density_view/by_density")

    # Create a dictionary to store the density value and associated areas
    density_dict = {}
    for row in view:
        # Skip entries where the density is "null"
        if row.key == "null":
            continue

        if row.key in density_dict:
            density_dict[row.key].append({
                'name': row.value['sa2_name_2016'],
                'code': row.value['sa2_maincode_2016']
            })
        else:
            density_dict[row.key] = [{
                'name': row.value['sa2_name_2016'],
                'code': row.value['sa2_maincode_2016']
            }]

    # Sort the density and get top 5 and bottom 5
    sorted_density_list = sorted(density_dict.items(), key=lambda x: x[0])

    # convert top and bottom density lists to desired format
    top_5_density = [{"name": area['name'], "value": float(density)} for density, areas in sorted_density_list[-25:] for
                     area in areas]
    bottom_5_density = [{"name": area['name'], "value": float(density)} for density, areas in sorted_density_list[:25]
                        for area in areas]

    meta = {
        'name': 'sa2',
        'value': 'population density (persons/km^2)'
    }

    return {"meta": meta, 'top data': top_5_density, 'bottom data': bottom_5_density}


#######################################################################################################################
#       scenario 8.1 Twitter avg senti vs suburb
#######################################################################################################################

twitter_db = couch['v9_all_data']
twitter_avgsenti_map = """
function(doc) {
    if ('avgsenti' in doc) {
        emit(doc._id, doc.avgsenti);
    }
}
"""

# Create the view
avg_senti_view_id = "_design/avg_senti_view"
if avg_senti_view_id in twitter_db:
    print("avg_senti_view_id Design document already exists. Deleting it.")
    twitter_db.delete(twitter_db[avg_senti_view_id])

print("Creating avg_senti_view_id Design document.")
twitter_db.save({
    "_id": avg_senti_view_id,
    "views": {
        "avgSenti": {
            "map": twitter_avgsenti_map,
        }
    }
})


@app.route('/avg_senti', methods=['GET'])
def avg_senti():
    # Fetch the view
    view = twitter_db.view("avg_senti_view/avgSenti")

    results = []

    for row in view:
        results.append({
            'suburb': row['key'],
            'avgsenti': row['value'],
        })

    meta = {
        'name': 'sa2',
        'value': 'avg senti'
    }

    return {"meta": meta, 'data': results}


#######################################################################################################################
#       scenario 8.2 Twitter topics vs suburb
#######################################################################################################################
twitter_topics_uniquetwts_map = """
function(doc) {
    if ('topics' in doc && 'uniquetwts' in doc) {
        emit(doc._id, { 'topics': doc.topics, 'uniquetwts': doc.uniquetwts });
    }
}
"""

# Create the view
topics_uniquetwts_view_id = "_design/topics_uniquetwts_view"
if topics_uniquetwts_view_id in twitter_db:
    print("topics_uniquetwts_view_id Design document already exists. Deleting it.")
    twitter_db.delete(twitter_db[topics_uniquetwts_view_id])

print("Creating topics_uniquetwts_view_id Design document.")
twitter_db.save({
    "_id": topics_uniquetwts_view_id,
    "views": {
        "topicsUniquetwts": {
            "map": twitter_topics_uniquetwts_map,
        }
    }
})


@app.route('/topics_uniquetwts/', methods=['GET'])
@app.route('/topics_uniquetwts/<suburb>', methods=['GET'])
def topics_uniquetwts(suburb=None):
    # Fetch the view
    view = twitter_db.view("topics_uniquetwts_view/topicsUniquetwts")

    results = []

    for row in view:
        if suburb is None or suburb.lower() == row['key'].lower():
            results.append({
                'suburb': row['key'],
                'topics_uniquetwts': row['value'],
            })
            if suburb is not None:
                break

    if len(results) > 0:
        meta = {
            'name': 'sa2',
            'value': 'topics and unique tweets'
        }
        return {"meta": meta, 'data': results}
    else:
        return {"meta": {}, 'data': []}


#######################################################################################################################
#       scenario 8.3 Twitter topics total proportion
#######################################################################################################################
topicAll_map = """
function(doc) {
    if ('topics' in doc && 'uniquetwts' in doc) {
        var topics = doc.topics;
        var uniquetwts = doc.uniquetwts;
        for (var topic in topics) {
            emit(topic, topics[topic] * uniquetwts);
        }
    }
}
"""

topicAll_map_reduce = """
function(keys, values, rereduce) {
    return sum(values);
}
"""

# Create the view
topicAll_id = "_design/topicAll_map_view"
if topicAll_id in twitter_db:
    print("topicAll_id Design document already exists. Deleting it.")
    twitter_db.delete(twitter_db[topicAll_id])

print("Creating topics_uniquetwts_view_id Design document.")
twitter_db.save({
    "_id": topicAll_id,
    "views": {
        "topicAll": {
            "map": topicAll_map,
            "reduce": topicAll_map_reduce
        }
    }
})

twitter_uniquetwts_total_map = """
function(doc) {
    if ('uniquetwts' in doc) {
        emit(null, doc.uniquetwts);
    }
}
"""

twitter_uniquetwts_total_reduce = """
function(keys, values, rereduce) {
    return sum(values);
}
"""

uniquetwts_total_id = "_design/uniquetwts_total_view"
if uniquetwts_total_id in twitter_db:
    print("uniquetwts_total_id Design document already exists. Deleting it.")
    twitter_db.delete(twitter_db[uniquetwts_total_id])

print("Creating uniquetwts_total_id Design document.")
twitter_db.save({
    "_id": uniquetwts_total_id,
    "views": {
        "uniquetwtsTotal": {
            "map": twitter_uniquetwts_total_map,
            "reduce": twitter_uniquetwts_total_reduce
        }
    }
})


@app.route('/topics_all_proportion', methods=['GET'])
def topics_all_proportion():
    uniquetwts_total = 0
    for row in twitter_db.view('uniquetwts_total_view/uniquetwtsTotal'):
        uniquetwts_total += row.value

    results = []
    for row in twitter_db.view('topicAll_map_view/topicAll', group=True):
        if row.key is not None:  # only include records with a topic
            results.append({'topic': row.key, 'proportion': row.value / uniquetwts_total})
    return jsonify(results)


#######################################################################################################################
#       scenario 9.1 twitter for correlation plot (senti vs sports)
#######################################################################################################################

twitter_db = couch['v9_all_data']

twitter_avgsenti_sports_map = """
function(doc) {
    if ('sports' in doc && 'avgsenti' in doc) {
        emit(doc._id, [doc.avgsenti, doc.sports]);
    }
}
"""

# Create the view
avgsenti_sports_view_id = "_design/avgsenti_sports_view"
if avgsenti_sports_view_id in twitter_db:
    print("avgsenti_sports_view_id Design document already exists. Deleting it.")
    twitter_db.delete(twitter_db[avgsenti_sports_view_id])

print("Creating avgsenti_sports_view_id Design document.")
twitter_db.save({
    "_id": avgsenti_sports_view_id,
    "views": {
        "avgSentiSports": {
            "map": twitter_avgsenti_sports_map,
        }
    }
})


@app.route('/senti_sports', methods=['GET'])
def senti_sports():
    # Fetch the view
    view = twitter_db.view("avgsenti_sports_view/avgSentiSports")

    left_values = []
    right_values = []

    for row in view:
        if row['value'][0] and row['value'][1]:
            left_values.append(row['value'][0])
            right_values.append(row['value'][1])

    correlation = np.corrcoef(left_values, right_values)[0, 1] if len(left_values) == len(right_values) else 0

    results = []
    for row in view:
        results.append({
            'suburb': row['key'],
            'avgsenti_sports': row['value'],
        })

    meta = {
        'name': 'sa2',
        'value': 'avg senti and sports',
        'correlation': correlation
    }

    return {"meta": meta, 'data': results}


#######################################################################################################################
#       scenario 9.2 twitter for correlation plot (senti vs median income)
#######################################################################################################################
twitter_avgsenti_income_map = """
function(doc) {
    if ('median income' in doc && 'avgsenti' in doc) {
        emit(doc._id, [doc.avgsenti, doc["median income"]]);
    }
}
"""

# Create the view
avgsenti_income_view_id = "_design/avgsenti_income_view"
if avgsenti_income_view_id in twitter_db:
    print("avgsenti_income_view_id Design document already exists. Deleting it.")
    twitter_db.delete(twitter_db[avgsenti_income_view_id])

print("Creating avgsenti_income_view_id Design document.")
twitter_db.save({
    "_id": avgsenti_income_view_id,
    "views": {
        "avgSentiIncome": {
            "map": twitter_avgsenti_income_map,
        }
    }
})


@app.route('/senti_income', methods=['GET'])
def senti_income():
    # Fetch the view
    view = twitter_db.view("avgsenti_income_view/avgSentiIncome")

    results = []

    for row in view:
        results.append({
            'suburb': row['key'],
            'avgsenti_income': row['value'],
        })

    left_values = []
    right_values = []

    for row in view:
        if row['value'][0] and row['value'][1]:
            left_values.append(row['value'][0])
            right_values.append(row['value'][1])

    correlation = np.corrcoef(left_values, right_values)[0, 1] if len(left_values) == len(right_values) else 0

    meta = {
        'name': 'sa2',
        'value': 'avg senti and income',
        'correlation': correlation
    }

    return {"meta": meta, 'data': results}


#######################################################################################################################
#       scenario 9.3 twitter for correlation plot (senti vs median age)
#######################################################################################################################
twitter_avgsenti_age_map = """
function(doc) {
    if ('median age' in doc && 'avgsenti' in doc) {
        emit(doc._id, [doc.avgsenti, doc["median age"]]);
    }
}
"""

# Create the view
avgsenti_age_view_id = "_design/avgsenti_age_view"
if avgsenti_age_view_id in twitter_db:
    print("avgsenti_age_view_id Design document already exists. Deleting it.")
    twitter_db.delete(twitter_db[avgsenti_age_view_id])

print("Creating avgsenti_age_view_id Design document.")
twitter_db.save({
    "_id": avgsenti_age_view_id,
    "views": {
        "avgSentiAge": {
            "map": twitter_avgsenti_age_map,
        }
    }
})


@app.route('/senti_age', methods=['GET'])
def senti_age():
    # Fetch the view
    view = twitter_db.view("avgsenti_age_view/avgSentiAge")

    results = []

    for row in view:
        results.append({
            'suburb': row['key'],
            'avgsenti_age': row['value'],
        })

    left_values = []
    right_values = []

    for row in view:
        if row['value'][0] and row['value'][1]:
            left_values.append(row['value'][0])
            right_values.append(row['value'][1])

    correlation = np.corrcoef(left_values, right_values)[0, 1] if len(left_values) == len(right_values) else 0

    meta = {
        'name': 'sa2',
        'value': 'avg senti and age',
        'correlation': correlation
    }

    return {"meta": meta, 'data': results}


#######################################################################################################################
#       scenario 9.4 twitter for correlation plot (senti vs transport CAI)
#######################################################################################################################
twitter_avgsenti_transport_map = """
function(doc) {
    if ('transport CAI' in doc && 'avgsenti' in doc) {
        emit(doc._id, [doc.avgsenti, doc["transport CAI"]]);
    }
}
"""

# Create the view
avgsenti_transport_view_id = "_design/avgsenti_transport_view"
if avgsenti_transport_view_id in twitter_db:
    print("avgsenti_transport_view_id Design document already exists. Deleting it.")
    twitter_db.delete(twitter_db[avgsenti_transport_view_id])

print("Creating avgsenti_transport_view_id Design document.")
twitter_db.save({
    "_id": avgsenti_transport_view_id,
    "views": {
        "avgSentiTransport": {
            "map": twitter_avgsenti_transport_map,
        }
    }
})


@app.route('/senti_transport', methods=['GET'])
def senti_transport():
    # Fetch the view
    view = twitter_db.view("avgsenti_transport_view/avgSentiTransport")

    results = []

    for row in view:
        results.append({
            'suburb': row['key'],
            'avgsenti_transport': row['value'],
        })

    left_values = []
    right_values = []

    for row in view:
        if row['value'][0] and row['value'][1]:
            left_values.append(row['value'][0])
            right_values.append(row['value'][1])

    correlation = np.corrcoef(left_values, right_values)[0, 1] if len(left_values) == len(right_values) else 0

    meta = {
        'name': 'sa2',
        'value': 'avg senti and transport',
        'correlation': correlation
    }

    return {"meta": meta, 'data': results}


#######################################################################################################################
#       scenario 9.5 twitter for correlation plot (senti vs population density)
#######################################################################################################################
twitter_avgsenti_population_map = """
function(doc) {
    if ('population density' in doc && 'avgsenti' in doc) {
        var populationDensity = parseFloat(doc["population density"]);
        if (!isNaN(populationDensity)) {
            emit(doc._id, [doc.avgsenti, populationDensity]);
        }
    }
}
"""

# Create the view
avgsenti_population_view_id = "_design/avgsenti_population_view"
if avgsenti_population_view_id in twitter_db:
    print("avgsenti_population_view_id Design document already exists. Deleting it.")
    twitter_db.delete(twitter_db[avgsenti_population_view_id])

print("Creating avgsenti_population_view_id Design document.")
twitter_db.save({
    "_id": avgsenti_population_view_id,
    "views": {
        "avgSentiPopulation": {
            "map": twitter_avgsenti_population_map,
        }
    }
})


@app.route('/senti_population', methods=['GET'])
def senti_population():
    # Fetch the view
    view = twitter_db.view("avgsenti_population_view/avgSentiPopulation")

    results = []

    for row in view:
        results.append({
            'suburb': row['key'],
            'avgsenti_population': row['value'],
        })

    left_values = []
    right_values = []

    for row in view:
        if row['value'][0] and row['value'][1]:
            left_values.append(row['value'][0])
            right_values.append(row['value'][1])

    correlation = np.corrcoef(left_values, right_values)[0, 1] if len(left_values) == len(right_values) else 0

    meta = {
        'name': 'sa2',
        'value': 'avg senti and population density',
        'correlation': correlation
    }

    return {"meta": meta, 'data': results}


#######################################################################################################################
#       scenario 9.6 twitter for correlation plot (senti vs crime)
#######################################################################################################################
twitter_avgsenti_crime_map = """
function(doc) {
    if ('crime' in doc && 'avgsenti' in doc) {
        var crimcnt = doc["crime"];
        if (!isNaN(crimcnt)) {
            emit(doc._id, [doc.avgsenti, crimcnt]);
        }
    }
}
"""

# Create the view
avgsenti_crime_view_id = "_design/avgsenti_crime_view"
if avgsenti_crime_view_id in twitter_db:
    print("avgsenti_crime_view_id Design document already exists. Deleting it.")
    twitter_db.delete(twitter_db[avgsenti_crime_view_id])

print("Creating avgsenti_crime_view_id Design document.")
twitter_db.save({
    "_id": avgsenti_crime_view_id,
    "views": {
        "avgSentiCrime": {
            "map": twitter_avgsenti_crime_map,
        }
    }
})


@app.route('/senti_crime', methods=['GET'])
def senti_crime():
    # Fetch the view
    view = twitter_db.view("avgsenti_crime_view/avgSentiCrime")

    results = []

    for row in view:
        results.append({
            'suburb': row['key'],
            'avgsenti_crime': row['value'],
        })

    left_values = []
    right_values = []

    for row in view:
        if row['value'][0] and row['value'][1]:
            left_values.append(row['value'][0])
            right_values.append(row['value'][1])

    correlation = np.corrcoef(left_values, right_values)[0, 1] if len(left_values) == len(right_values) else 0

    meta = {
        'name': 'sa2',
        'value': 'avg senti and crime',
        'correlation': correlation
    }

    return {"meta": meta, 'data': results}


#######################################################################################################################
#       scenario 10 Mastodon topics total proportion
#######################################################################################################################

mastodon_db = couch['mastodon_test']
# Map function for counting occurrence of each topic
mas_topic_count_map = """
function(doc) {
    if (doc.topics) {
        doc.topics.forEach(function(topic) {
            emit(topic, 1);
        });
    }
}
"""

# Reduce function for summing up the counts
mas_topic_count_reduce = """
function(keys, values, rereduce) {
    return sum(values);
}
"""

# Create the view for topic count
mas_topic_count_view_id = "_design/topic_count_view"
if mas_topic_count_view_id in mastodon_db:
    print("mas_topic_count_view_id Design document already exists. Deleting it.")
    mastodon_db.delete(mastodon_db[mas_topic_count_view_id])

print("Creating mas_topic_count_view_id Design document.")
mastodon_db.save({
    "_id": mas_topic_count_view_id,
    "views": {
        "topicCount": {
            "map": mas_topic_count_map,
            "reduce": mas_topic_count_reduce
        }
    }
})

# Map function for counting the total number of documents
mas_total_docs_map = """
function(doc) {
    emit(null, 1);
}
"""

# Reduce function for summing up the counts
mas_total_docs_reduce = """
function(keys, values, rereduce) {
    return sum(values);
}
"""

# Create the view for total document count
mas_total_docs_view_id = "_design/total_docs_view"
if mas_total_docs_view_id in mastodon_db:
    print("mas_total_docs_view_id Design document already exists. Deleting it.")
    mastodon_db.delete(mastodon_db[mas_total_docs_view_id])

print("Creating mas_total_docs_view_id Design document.")
mastodon_db.save({
    "_id": mas_total_docs_view_id,
    "views": {
        "totalDocs": {
            "map": mas_total_docs_map,
            "reduce": mas_total_docs_reduce
        }
    }
})


@app.route('/mas_topics_proportion', methods=['GET'])
def mas_topics_proportion():
    total_docs = 0
    for row in mastodon_db.view('total_docs_view/totalDocs'):
        total_docs += row.value

    results = []
    for row in mastodon_db.view('topic_count_view/topicCount', group=True):
        if row.key is not None:  # only include records with a topic
            results.append({'topic': row.key, 'proportion': row.value / total_docs})
    return jsonify(results)


#######################################################################################################################
#       scenario 10.1 Mastodon topic real time predict, with time slot
#######################################################################################################################
latest_doc_map = """
function(doc) {
    if (doc.created_at) {
        var dateStr = doc.created_at.substring(0, 19) + 'Z';  // Cut the date string to second and append 'Z' for UTC time
        var timestamp = Date.parse(dateStr);
        emit(timestamp, { "content": doc.content, "topics": doc.topics, "url": doc.url, "sentiment_score": doc.sentiment_score });
    }
}
"""

# Create the view for getting the latest document
latest_doc_view_id = "_design/latest_doc_view"
if latest_doc_view_id in mastodon_db:
    print("latest_doc_view_id Design document already exists. Deleting it.")
    mastodon_db.delete(mastodon_db[latest_doc_view_id])

print("Creating latest_doc_view_id Design document.")
mastodon_db.save({
    "_id": latest_doc_view_id,
    "views": {
        "latestDoc": {
            "map": latest_doc_map,
        }
    }
})


@app.route('/mas_latest_doc', methods=['GET'])
def mas_latest_doc():
    results = mastodon_db.view('latest_doc_view/latestDoc', descending=True, limit=1)
    for row in results:
        data = row.value
        data['timestamp'] = datetime.fromtimestamp(row.key / 1000).strftime(
            '%Y-%m-%d %H:%M:%S')  # convert to human-readable date string
        return jsonify(data)
    return jsonify({"error": "No documents found"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
