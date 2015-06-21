"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import sys

OSMFILE = ""
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Pass", "Highway", "Cove", "Expressway", "Loop", "Way",
            "Path", "Interstate"]

# UPDATE THIS VARIABLE
mapping = {"st": "Street",
           "ave": "Avenue",
           "rd": "Road",
           "blvd": "Boulevard",
           "dr": "Drive",
           "cv": "Cove",
           "ct": "Court",
           "cir": "Circle",
           "ln": "Lane",
           "cr": "Circle",
           "hwy": "Highway",
           "pkwy": "Parkway",
           "dr": "Drive",
           "expway": "Expressway",
           "expwy": "Expressway",
           "ste": "Suite",
           "n": "North",
           "w": "West",
           "s": "South",
           "e": "East",
           "i": "Interstate",
           "h": "Highway",
           "ih": "Interstate Highway",
           "tx": "Texas",
           "us": "US",
           "fm": "Farm to Market Road",
           "farm-to-market": "Farm to Market",
           "ranch-to-market": "Ranch to Market",
           "rm": "Ranch to Market Road",
           "rr": "Ranch to Market Road",
           "bldg": "Building",
           "bld": "Building",
           "i-35": "Interstate 35",
           "ih-35": "Interstate Highway 35",
           "sb": "Southbound",
           "nb": "Northbound"
            }

def parse(filepath):
    OSMFILE = filepath
    street_types = audit(OSMFILE)
    pprint.pprint(dict(street_types))

    for street_type, ways in street_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name

# Looks 
def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    return street_types

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

# Update one street name
def update_name(name, mapping):
    keys = mapping.keys()
    
    split_name = name.split(" ")
    split_name = check(split_name)
        
    name = " ".join(fix_all_tokens(split_name, keys))
    return name

# Checks if there is more than one token: if so, check further
def check(split_name):
    if len(split_name) > 1:
        return split_name
    split_name = check_for_digit(split_name)
    return split_name

# Basically checks if street name is of form "I35" or "FM1431", rather than "I 35" or "FM 1431"
# If it is, then split the name where they meet, e.g. ["I35"] => ["I", "35"], and return
def check_for_digit(split_name):
    for i, char in enumerate(split_name[0]):
        if char.isdigit():
            return [split_name[0][:i], split_name[0][i:]]
    return split_name

# Once checking is done, we fix all the tokens in the split street name
def fix_all_tokens(token_list, keys):
    for i, token in enumerate(token_list):
        fixed = False
        token = token.translate(None, ".,").lower() # Removes all periods and commas
        token_list[i], fixed = try_to_map_token(keys, token) 
        if not fixed:
            token_list[i] = fix_token(token)
    return token_list

def try_to_map_token(keys, token):
    for key in keys:
        if token == key:
            return mapping[key], True
    return token, False

# If token not successfully mapped, then fix it in one of the following ways
def fix_token(token):
    if "ih-" in token:
        return token.replace("ih-", "Interstate Highway ")
    elif "#" in token:
        return fix_suite_number(token)
    else:
        return token.capitalize()

# Basically, lots of suites are titled "Suite #141" or "suite#141"
# I remove the pound sign and split the tokens if needed
def fix_suite_number(token):
    split = token.split("#")
    if split[0] == "" or split[0] == " ":
        return split[1]
    else:
        return " ".join(word.capitalize().strip() for word in split)
            


