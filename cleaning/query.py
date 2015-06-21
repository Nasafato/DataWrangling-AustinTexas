import pymongo
import pprint
import json
import sys

QUERY_FILE = "queries/queries.json"
query_list = []
query_dict = {}
collection_list = []

def get_db(dbname):
    client = pymongo.MongoClient()
    return client[dbname]

def select_query():
    db = get_db("osm")
    collection_name = select_collection(db)
    list_pipelines(QUERY_FILE)
    choice = input("Enter the number of the query you wish to perform: ")
    print
    if choice < 1 or choice > len(query_list):
        print("ERROR: out of bounds choice number")
        return
    pprint.pprint(query(db, query_dict[query_list[choice-1]]["pipeline"], collection_name))

def select_collection(db):
    global collection_list
    for tup in enumerate(db.collection_names(), start=1):
        collection_list.append(tup[1])
        print("\t{}. {}".format(tup[0], tup[1]))
    print
    choice = input("Enter the number of the collection you wish to perform queries on: ")
    print
    return collection_list[choice-1]

def list_pipelines(filepath):
    with open(filepath, "r") as f:
        global query_dict
        query_dict = json.load(f)
        print("Available MongoDB queries:")
        if len(query_list) == 0:
            for key, vaue in query_dict.iteritems():
                query_list.append(key)
        for tup in enumerate(query_list, start=1):
            print("\t{}. {}".format(tup[0], tup[1]))
        print
            
def query(db, pipeline, collection_name):
    result = db[collection_name].aggregate(pipeline)
    return result
    
