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
import csv
import pandas as pd
from collections import defaultdict
from geopy.geocoders import Nominatim

if __name__ == '__main__':

    couch = couchdb.Server('http://admin:password@localhost:5984/')
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






