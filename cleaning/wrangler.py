import glob, os
import sys
import audit
import classify
import data
import mapparser
import tags
import users
import query
import dbops

data_file_list = []
json_file_list = []

def initialize_data_file_list():
    global data_file_list
    data_file_list = [f for f in os.listdir("../data") if f.endswith(".osm")]

def list_data_files():
    print("\nListing data files...")
    global data_file_list
    for f in data_file_list:
        print("\t%s" % f)

# Counts the number of tags of each kind in the specified file
def parse_map_file_tags():
    filepath = select_file("osm")
    mapparser.parse(filepath)

# Counts the number of types of keys of each kind in the specified file
def parse_map_file_keys():
    filepath = select_file("osm")
    tags.parse(filepath)

# Gets the number of unique users who have contributed to the map
def get_unique_users():
    filepath = select_file("osm")
    users.parse(filepath)

# Audits the .osm file and shows fixes to faulty street names
def audit_file():
    filepath = select_file("osm")
    audit.parse(filepath)

# Parses the file into JSON format, using the fixes in audit_file()
def insert_data():
    filepath = select_file("osm")
    data.parse(filepath)

# Performs a MongoDB query
def perform_query():
    query.select_query()

# Changes the DBs in MongoDB
def operate_on_db():
    dbops.perform_change()

# Asks the user to select the file he/she wants to parse
def select_file(suffix):
    global data_file_list
    enumerate_files("osm")
    choice = input("Enter number of the file you wish to parse: ")
    choice -= 1

    if suffix == "osm":
        return "../data/{}".format(data_file_list[choice])
    elif suffix == "json":
        return "../data/{}".format(json_file_list[choice])
    else:
        return None

# Prints out all the files in numeric order
def enumerate_files(suffix):
    global data_file_list
    print("\nFile Choices")
    if suffix == "osm":
        for tup in enumerate(data_file_list, start=1):
            print("\t{}. {}".format(tup[0], tup[1]))
    elif suffix == "json":
        for tup in enumerate(json_file_list, start=1):
            print("\t{}. {}".format(tup[0], tup[1]))

# Taken from data.py: displays what the output file name will be
def display_output_file_form(file_in):
    split_file_path = file_in.split("/")
    file_name = split_file_path[-1]
    split_file_path[-1] = "{0}.json".format(file_name.split(".")[0])
    file_out = "/".join(split_file_path)

def list_options():
    print('-' * 60)
    print("Options:")
    print("\t1. List data files")
    print("\t2. Parse map file to get tags")
    print("\t3. Parse map file to get key types")
    print("\t4. Get number of unique users")
    print("\t5. Audit street names")
    print("\t6. Parse data into JSON format")
    print("\t7. Perform MongoDB query")
    print("\t8. Operate on databases")

def main():
    print("Alan Gou's Data Wrangling Driver for Austin, TX OSM Data")
    choice = -1

    initialize_data_file_list()

    while choice != 0: 
        list_options()
        choice = input("\nEnter number of command ('0' to quit): ")
        if choice == 1:
            list_data_files()
        elif choice == 2:
            parse_map_file_tags()
        elif choice == 3:
            parse_map_file_keys()
        elif choice == 4:
            get_unique_users()
        elif choice == 5:
            audit_file()
        elif choice == 6:
            insert_data()
        elif choice == 7:
            perform_query()
        elif choice == 8:
            operate_on_db()

if __name__ == "__main__":
    main()
