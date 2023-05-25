import os.path
import re
import json
import time
from collections import defaultdict
from collections import Counter
from mpi4py import MPI
import pandas as pd
import couchdb
import re
from collections import defaultdict
from geopy.geocoders import Nominatim
from shapely.geometry import Polygon, MultiPolygon


if __name__ == '__main__':
    start_time = time.time()
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    couch = couchdb.Server('http://admin:admin@172.26.135.221:5984')

    # if rank == 0:

    # db_name = 'network'
    # if db_name not in couch:
    #     db = couch.create(db_name)
    # else:
    #     db = couch[db_name]
    #
    # geolocator = Nominatim(user_agent="tttk8523", timeout=3)
    #
    # with open("performance_australia_fixed_2020_q4-1090446208275030516.json", "r") as file:
    #     data = json.load(file)
    #
    # for i in data['features']:
    #
    #     properties = i['properties']
    #     row = i['geometry']['coordinates']
    #     g = MultiPolygon([Polygon(r[0]) for r in row])
    #     Latitude = g.centroid.y
    #     Longitude = g.centroid.x
    #     comb = str(Latitude) + "," + str(Longitude)
    #     location = str(geolocator.reverse(comb))
    #     if 'Victoria' in location:
    #         properties['Location'] = location
    #         doc_id, doc_rev = db.save(properties)
    if rank == 1:
        sports_file = 'simplified_vic_sport_and_recreation_2015.json'

        with open("simplified_vic_sport_and_recreation_2015.json", "r") as file:
            data = json.load(file)

        # Count unique objectids for each sportsplayed value

        facility_sub = defaultdict(int)
        sports_sub = defaultdict(dict)



        for i in data:
            facility_sub[i['suburbtown']] += 1
            if i['sportsplayed'] in sports_sub[i['suburbtown']]:
                sports_sub[i['suburbtown']][i['sportsplayed']] += 1
            else:
                sports_sub[i['suburbtown']][i['sportsplayed']] = 1

        db_name = 'total_number_of_facility_suburb'
        if db_name not in couch:
            db = couch.create(db_name)
        else:
            db = couch[db_name]
        for i in facility_sub:
            cur_dic = {}
            cur_dic['Suburb'] = i
            cur_dic['Number_of_Facility'] = facility_sub[i]
            doc_id, doc_rev =db.save(cur_dic)

        db_name = 'sports_facility_suburb'
        if db_name not in couch:
            db = couch.create(db_name)
        else:
            db = couch[db_name]

        for i in sports_sub:
            sports_sub[i]['Suburb'] = i
            db.save(sports_sub[i])

    if rank == 2:
        transport_file = 'Melbourne_Transport.json'
        db_name = 'transport'
        if db_name not in couch:
            db = couch.create(db_name)
        else:
            db = couch[db_name]

        geolocator = Nominatim(user_agent="CCC_assignment")

        with open("Melbourne_Transport.json", "r") as file:
            data = json.load(file)

        for i in data:
            Longitude, Latitude = data[i]['coordinates']
            comb = str(Latitude) + "," + str(Longitude)
            location = geolocator.reverse(comb)
            suburb = str(location).split(",")[2][1:]
            data[i]['coordinates'] = suburb
            db.save(data[i])

    if rank == 3:
        db_name = 'employment'
        if db_name not in couch:
            db = couch.create(db_name)
        else:
            db = couch[db_name]

        df = pd.read_csv("employment_brief.csv", low_memory=False)
        header = list(df.columns)[1:]

        for index, row in df.iterrows():
            dic = {}
            if df.loc[index]['ste_name11'] != "Victoria":
                continue
            idx = 0
            for i in df.loc[index][1:]:
                dic[header[idx]] = i
                idx += 1

            for i in dic:
                try:
                    dic[i] = int(dic[i])
                except:
                    continue

            db.save(dic)

