import os.path
import json
import time
from collections import defaultdict
from mpi4py import MPI
import pandas as pd
import couchdb
import re
from shapely.geometry import Point
import geopandas
from tweet_topic_classification import topic_classifier, load_model
import os



def read_data(path):
    """
    Read the data from the json file
    :param path: the path of the json file
    :return: the data
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def generate_area_dict(data):
    """
    Generate the area dictionary
    :param data: the area data
    :return: the area dictionary
    """
    area_dict = {}
    for area in data:
        gcc = data[area]['gcc']
        # Only keep the greater capital city
        if not re.search("\dr[a-zA-Z]+", gcc):
            area_dict[area] = gcc
    return area_dict


def check_area_in_great_city(area, great_city):
    """
    Check if the area is in the great city
    :param area: the area name
    :param great_city: the great city list
    :return: True or False
    """
    area = area.split(',')[0].lower()
    if area in great_city:
        return True
    else:
        return False


def sort_dict_by_values(d):
    """
    Sort the dictionary by values
    :param d: the dictionary
    :return: the sorted dictionary
    """
    sorted_dict = dict(sorted(d.items(), key=lambda x: x[1], reverse=True))
    return sorted_dict


def task1_dict2df(task1_dict):
    """
    Convert the task1 dictionary to dataframe
    :param task1_dict: the task1 dictionary
    :return: the dataframe
    """
    li1 = []
    count = 0
    cur_rank = 1
    max_tweets_count = list(task1_dict.values())[0]

    for i in task1_dict:
        id = i
        if task1_dict[id] < max_tweets_count:
            max_tweets_count = task1_dict[id]
            cur_rank += count
            count = 1
        else:
            count += 1
        if cur_rank > 10:
            break
        rank = '#' + str(cur_rank)
        li1.append([rank, id, task1_dict[id]])
    task1_df = pd.DataFrame(li1)
    task1_df.columns = ['Rank', 'Author Id', 'Number of Tweets Made']
    return task1_df


def task2_dict2df(task2_dict):
    """
    Convert the task2 dictionary to dataframe
    :param task2_dict: the task2 dictionary
    :return: the dataframe
    """
    li2 = []
    greater_city = {'1gsyd': 'Greater Sydney',
                    '2gmel': "Greater Melbourne",
                    "3gbri": "Greater Brisbane",
                    "4gade": "Greater Adelaide",
                    "5gper": "Greater Perth",
                    "6ghob": "Greater Hobart",
                    "7gdar": "Greater Darwin",
                    "8acte": "Greater Canberra",
                    "9oter": "Great Other Territories"
                    }
    for i in task2_dict:
        city = f'{i}({greater_city[i]})'
        li2.append([city, task2_dict[i]])

    task2_df = pd.DataFrame(li2)
    task2_df.columns = ['Greater Capital City', 'Number of Tweets Made']
    return task2_df


def task3_dict2df(task3_dict):
    """
    Convert the task3 dictionary to dataframe
    :param task3_dict: the task3 dictionary
    :return: the dataframe
    """
    count = 0
    cur_city_num = task3_dict[0][1][0]
    cur_tweets_num = task3_dict[0][1][1]
    cur_rank = 1

    li3 = []
    for i in task3_dict:
        author_id = i[0]
        city_num = i[1][0]
        tweets_num = i[1][1]
        city_tweets = ''

        if city_num < cur_city_num:
            cur_city_num = city_num
            cur_tweets_num = tweets_num
            cur_rank += count
            count = 1
        else:
            if tweets_num < cur_tweets_num:
                cur_tweets_num = tweets_num
                cur_rank += count
                count = 1
            else:
                count += 1

        if cur_rank > 10:
            break
        rank = '#' + str(cur_rank)
        total = '#' + str(i[1][1]) + ' tweets ' + '- '

        city_tweets += total
        cur_list = []
        for j in i[1][2]:
            if i[1][2][j] != 0:
                jj = str(i[1][2][j]) + j[1:]
                combine = '#'
                combine += jj
                cur_list.append(combine)
        cur = ', '.join(map(str, cur_list))
        city_tweets += cur
        col3 = str(city_num) + ' (' + city_tweets + ')'
        li3.append([rank, author_id, col3])

    task3_df = pd.DataFrame(li3)
    task3_df.columns = ['Rank', 'Author Id', 'Number of Unique City Locations and #Tweets']
    return task3_df


if __name__ == '__main__':


    start_time = time.time()
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

    # Read the sal data and generate the area dictionary
    sal_file = 'sal.json'
    area_data = read_data(sal_file)
    area_dict = generate_area_dict(area_data)

    # Initialize the variables
    author_tweets_count = defaultdict(int)
    author_city_tweets_count = {}
    gcc_tweets_count = {'1gsyd': 0,
                        '2gmel': 0,
                        "3gbri": 0,
                        "4gade": 0,
                        "5gper": 0,
                        "6ghob": 0,
                        "7gdar": 0,
                        "8acte": 0,
                        "9oter": 0
                        }
    author = ''
    place = ''
    author_id_string = """      "author_id":"""""
    place_name_string = """          "full_name":"""""

    # Divide the file into several parts where the number of parts are equal to the number of processes
    # So that each process can handle one part of the file simultaneously
    twitter_file = 'twitter-huge.json'
    total_bytes = os.path.getsize(twitter_file)
    each_bytes = total_bytes // size
    start_position = rank * each_bytes
    end_position = (rank + 1) * each_bytes
    couch = couchdb.Server('http://admin:password@localhost:5984')
    db_name = 'twitter_loc'
    if db_name not in couch:
        db = couch.create(db_name)
    else:
        db = couch[db_name]

    # vic_localities.shp
    aus_poas = geopandas.read_file('vic_localities.shp')
    db_name = 'twitter_huge'
    if db_name not in couch:
        db = couch.create(db_name)
    else:
        db = couch[db_name]


    # aus_poas.shp
    # aus_poas = geopandas.read_file('aus_poas.shp')

    # Read the twitter data
    with open(twitter_file, 'r', encoding='utf-8') as f:
        new_line = f.readline()
        # Find the start position of the file
        f.seek(start_position)
        while True:

            new_line = f.readline()


            id_found = False
            place_found = False
            location_found = False
            sentiment_found = False
            content_found = False
            token_found = False
            language_found = False
            tag_found = False
            bbox_found = False
            topic_found = False


            # End the loop if reach the end of the file
            if not new_line:
                break

            try:
                # find author id
                i_s = new_line.index("author_id")
                id_found = True

                cur_i = new_line[i_s:].split(",")[0]
                id = cur_i.split(":")[1][1:-1]

                # find place name and contain only suburb in VIC
                # p_s = new_line.index("full_name")
                # cur_p = new_line[p_s:].split(',"')[0]
                # place = cur_p.split(':')[1][1:-1]
                #
                # if "Victoria" in place:
                #     place_found = True

                # find sentiment score
                s_s = new_line.index("sentiment")
                sentiment_found = True
                cur_s = new_line[s_s:].split("}")[0]

                sentiment = float(cur_s.split(":")[1])

                # find twitter content

                c_s = new_line.index('"text":')
                c_e = new_line.index("sentiment") - 2
                content_found = True

                cur_c = new_line[c_s:c_e]
                text = cur_c.split('":')[1][1:-1]

                # find language
                l_s = new_line.index('"lang"')
                cur_l = new_line[l_s:].split(",")[0]
                language = cur_l.split(":")[1][1:-1]

                if language == 'en':
                    language_found = True

                # find bounding box
                bbox_s = new_line.index('"bbox":[')
                cur_bbox = new_line[bbox_s:].split('],')[0]
                raw_bbox = cur_bbox.split(":[")[1]

                bbox = raw_bbox.split(",")
                cor = Point((float(bbox[0]) + float(bbox[2]))/2 , (float(bbox[1]) + float(bbox[3]))/2)
                cor_j = (cor.x,cor.y)

                # vic_localities.shp
                for i in aus_poas[['LOC_NAME', 'geometry']].itertuples():
                    if cor.within(i[2]):
                        postcode = i[1]
                        bbox_found = True
                        break
            except:

                continue

            if id_found and sentiment_found and content_found and language_found and bbox_found:
                test_dic = {"Author_Id": id,
                            "Sentiment_Score": sentiment,
                            "Text": text,
                            "Language": language,
                            "Coordinate": cor_j,
                            "Suburb": postcode
                            }
                # doc_id, doc_rev = db.save(test_dic)

                author = ''
                place = ''
                # Break if the current position is larger than the end position
                if f.tell() >= end_position:
                    break

