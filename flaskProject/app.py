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
public_transport_db = couch['transport']
employment_db = couch['employment']
income_db = couch['income']
population_db = couch['population_sa2_data']
age_db = couch['median_age_sa2_data']
twitter_db = couch['']
mastodon_db = couch['']
crime_db = couch['crime_data']


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
    crime_results = [dict(lga_name11=row.key, total=row.value["total"], lga_code11=row.value["lga_code11"]) for row in
                     crime_view]
    crime_results.sort(key=lambda x: x['total'], reverse=True)
    top_5_crime = crime_results[:5]
    bottom_5_crime = crime_results[-5:]

    # Return the results as JSON
    return {'Top 5': top_5_crime, 'Bottom 5': bottom_5_crime}


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
    # Get ages
    age_view = age_db.view('age_view/by_median_age')
    age_results = [dict(sa2_name=row.value, median_age=row.key) for row in age_view]
    age_results.sort(key=lambda x: x['median_age'], reverse=True)
    top_5_age = age_results[:5]
    bottom_5_age = age_results[-5:]

    # Return the results as JSON
    return {'Top 5': top_5_age, 'Bottom 5': bottom_5_age}


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


@app.route('/public_transport_top_bottom/', methods=['GET'])
def public_transport_top_bottom():
    # Get public transport data
    public_transport_view = public_transport_db.view('composite_index_view/by_composite_index')
    public_transport_dict = {}
    for row in public_transport_view:
        if row.value in public_transport_dict:
            public_transport_dict[row.value].append(row.key)
        else:
            public_transport_dict[row.value] = [row.key]

    # Calculate average composite_index for each coordinates
    avg_composite_index_dict = {coordinates: sum(values)/len(values) for coordinates, values in public_transport_dict.items()}

    # Sort by composite_index and get top 5 and bottom 5
    sorted_composite_index_list = sorted(avg_composite_index_dict.items(), key=lambda x: x[1], reverse=True)
    top_5_public_transport = sorted_composite_index_list[:5]
    bottom_5_public_transport = sorted_composite_index_list[-5:]

    # Return the results as JSON
    return {'Top 5': top_5_public_transport, 'Bottom 5': bottom_5_public_transport}


#######################################################################################################################
#       scenario 7 The top5 and bot 5 population density   sa2name sa2density
#
#######################################################################################################################
get_top_density_func = """
function (doc) {
  if (doc[" population_density_as_at_30_june_population_density_personskm2"] && doc[" sa2_name_2016"] && doc[" sa2_maincode_2016"]) {
    emit(doc[" population_density_as_at_30_june_population_density_personskm2"], {sa2_name_2016: doc[" sa2_name_2016"], sa2_maincode_2016: doc[" sa2_maincode_2016"]});
  }
}
"""


# Create the view
top_density_view_id = "_design/top_density_view"
if top_density_view_id in population_db:
    print("top_density_view Design document already exists. Updating it now.")
    # design_doc = population_db[top_density_view_id]
    #
    # # Update the view
    # design_doc['views']['by_density'] = {"map": get_top_density_func}
    # # Save the updated design document back to the database
    # population_db.save(design_doc)
else:
    print("top_density_view Design document does not exist. Creating it now.")
    population_db.save({
        "_id": top_density_view_id,
        "views": {
            "by_density": {
                "map": get_top_density_func
            }
        }
    })


@app.route('/population_density', methods=['GET'])
def population_density():
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
    sorted_density_list = sorted(density_dict.items(), key=lambda x: x[0], reverse=True)
    top_5_density = sorted_density_list[:5]
    bottom_5_density = sorted_density_list[-5:]

    return {'Top 5': top_5_density, 'Bottom 5': bottom_5_density}



#######################################################################################################################
#       scenario 8 The top5 and bot 5 internet
#
#######################################################################################################################

# Map function
get_twitter_total_map_func = '''function(doc) {
    if (doc.Place && doc["Sentiment Score"]) {
        var total = parseFloat(doc["Sentiment Score"]);
        emit(doc.Place, total);
    }
}'''



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


#######################################################################################################################
#       scenario 9 Twitter
#
#######################################################################################################################






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
