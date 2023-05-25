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
from shapely.geometry import Point
import geopandas

if __name__ == '__main__':
    start_time = time.time()
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    aus_poas = geopandas.read_file('vic_localities.shp')


    transport_file = 'Melbourne_Transport.json'
    couch = couchdb.Server('http://admin:password@localhost:5984/')
    db_name = 'transport_suburb'
    if db_name not in couch:
        db = couch.create(db_name)
    else:
        db = couch[db_name]

    geolocator = Nominatim(user_agent="CCC_assignment")

    with open("Melbourne_Transport.json", "r") as file:
        data = json.load(file)



    for i in data:
        Longitude,Latitude = data[i]['coordinates']
        cor = Point(Longitude,Latitude)
        for j in aus_poas[['LOC_NAME', 'geometry']].itertuples():
            if cor.within(j[2]):
                data[i]['Suburb'] = j[1]
                break
        db.save(data[i])
        # comb = str(Latitude) + "," + str(Longitude)
        # location = geolocator.reverse(comb)
        # suburb = str(location).split(",")[2][1:]
        # data[i]['coordinates'] = suburb





