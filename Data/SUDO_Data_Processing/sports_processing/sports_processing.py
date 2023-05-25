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

if __name__ == '__main__':
    start_time = time.time()
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()


    sports_file = 'simplified_vic_sport_and_recreation_2015.json'
    couch = couchdb.Server('http://admin:password@localhost:5984/')



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

    for i in facility_sub:
        cur_dic = {}
        cur_dic['Suburb'] = i
        cur_dic['Number_of_Facility'] = facility_sub[i]
        print(cur_dic)

    for i in sports_sub:
        sports_sub[i]['Suburb'] = i
        print(sports_sub[i])
