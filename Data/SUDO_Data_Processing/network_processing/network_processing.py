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


    couch = couchdb.Server('http://admin:password@localhost:5984/')
    db_name = 'network'
    if db_name not in couch:
        db = couch.create(db_name)
    else:
        db = couch[db_name]

    geolocator = Nominatim(user_agent="tttk8523", timeout=3)

    with open("performance_australia_fixed_2020_q4-1090446208275030516.json", "r") as file:
        data = json.load(file)



    for i in data['features']:

        properties = i['properties']
        row = i['geometry']['coordinates']
        g = MultiPolygon([Polygon(r[0]) for r in row])
        Latitude = g.centroid.y
        Longitude = g.centroid.x
        comb = str(Latitude) + "," + str(Longitude)
        location = str(geolocator.reverse(comb))
        if 'Victoria' in location:
            properties['Location'] = location
            doc_id, doc_rev = db.save(properties)






