import pymongo
import sys

collection_list = []

def perform_change():
    db = get_db("osm")
    collection_choice = select_collection(db)
    if collection_choice == 0:
        return
    choice = raw_input("Type 'yes' if you want to drop this collection or 'no' if you want to return: ")
    if choice == "yes":
        db.drop_collection(collection_list[collection_choice])
    else:
        return

def select_collection(db):
    global collection_list
    for tup in enumerate(db.collection_names(), start=1):
        collection_list.append(tup[1])
        print("\t{}. {}".format(tup[0], tup[1]))
    print
    choice = input("Enter the number of the collection you wish to perform operations on ('0' to quit): ")
    print
    return choice-1

def get_db(dbname):
    client = pymongo.MongoClient()
    return client[dbname]
    

