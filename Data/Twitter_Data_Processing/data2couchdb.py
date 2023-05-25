import json
import couchdb
from mpi4py import MPI

if __name__ == '__main__':
    couch = couchdb.Server('http://admin:admin@172.26.135.221:5984/')
    try:
        db = couch.create('tweets_processed')
    except:
        db = couch['tweets_processed']

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    with open('processed_twitter.json', 'rb') as f:
        data = json.load(f)
        n = len(data)
        start_position = rank * n // size
        end_position = (rank + 1) * n // size
        data_each_process = data[start_position:end_position]
        for item in data_each_process:
            db.save(item)


