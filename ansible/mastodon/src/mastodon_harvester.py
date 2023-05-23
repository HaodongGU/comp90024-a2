import couchdb
import requests
from mastodon import Mastodon, StreamListener
from mastodon_toots_processing import toot_processing

import json

with open('mastodon_info.json', 'r') as f:
    config = json.load(f)

    MASTODON_ACCESS_TOKEN = config["token"]
    toot_count = 0
    toots = []

    m = Mastodon(
        api_base_url=config["url"],
        access_token=MASTODON_ACCESS_TOKEN
    )


    class StopStreamingException(Exception):
        pass


    def upload2couchdb(toot):
        couch = couchdb.Server('http://admin:admin@172.26.134.190:5984/')
        try:
            db = couch.create(config["db"])
        except:
            db = couch[config["db"]]
        db.save(toot)


    def crawl_request():
        base_url = config["url"]+'/api/v1/'
        header = {
            "Authorization": f"Bearer {MASTODON_ACCESS_TOKEN}"
        }
        r = requests.get(base_url + '/accounts/verify_credentials', headers=header)
        print(r.json())


    class Listener(StreamListener):

        def __init__(self, count, upper_limit):
            super().__init__()
            self.count = count
            self.upper_limit = upper_limit

        def on_update(self, status):
            if self.count == 0:
                print("Start harvesting.....")
            if (status["language"]) == "en":
                toot_processed = toot_processing(status)
                upload2couchdb(toot_processed)
                self.count += 1
            if self.count % 50 == 0:
                print("Has harvested {} toots.".format(self.count))
            # global toot_count
            # toot_count += 1
            # if toot_count == 10:
            #     # exit(0)
            #     # return json.dumps(status, indent=2, sort_keys=True, default=str)
            #     toots.append(status)
            #     raise StopStreamingException("Received 1000 toots. Stopping streaming.")


    if __name__ == '__main__':
        # crawl_request()

        listener = Listener(0, 10)
        m.stream_public(listener)
        # try:
        #     m.stream_public(listener)
        # except StopStreamingException as e:
        #     print(e)
        #     for toot in toots:
        #         print(toot['content'])
        #         print()
