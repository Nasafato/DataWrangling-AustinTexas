#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json
import sys
import audit
"""
{
"id": "2406124091",
"type": "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}
"""

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

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
POS = ["lat", "lon"]


def parse(filename):
    process_map(filename, False)

def process_map(file_in, pretty = False):
    split_file_path = file_in.split("/")
    file_name = split_file_path[-1]
    split_file_path[-1] = "{0}.json".format(file_name.split(".")[0])
    file_out = "/".join(split_file_path)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")

# Turns XML formatted node into an appropriately formatted JSON dict,
# which can be readily imported into MongoDB
# Note that we only care about 'node' or 'way' elements
def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way":
        node = get_attrib(node, element)
        node = insert_tag(node, element)
        return node
    else:
        return None

# Creates the 'created' and 'pos' dict fields for the node
def get_attrib(node, element):
    keys = element.keys()
    node["pos"] = [0, 0]
    node["created"] = {}
    
    for key in keys:
        if key in CREATED:
            node["created"][key] = element.attrib[key]
        elif key == "lat":
            node["pos"][0] = float(element.attrib[key])
        elif key == "lon":
            node["pos"][1] = float(element.attrib[key])
        else:
            node[key] = element.attrib[key]

    node["type"] = element.tag

    if node["pos"] == [0, 0]: # No 'lat' or 'lon' fields in XML node
        del(node["pos"])
    if node["created"] == {}: # No 'created' fields in XML node
        del(node["created"])

    return node

# Parses the tags of the element and inserts them appropriately into the
# node dictionary object
def insert_tag(node, element):
    if element.tag == "way":
        node = get_refs(node, element)
        
    for tag in element.iter("tag"):
        split_tokens = str.split(tag.attrib["k"],":")
        if len(split_tokens) == 1: # if no colons in tag name
            node[split_tokens[0]] = tag.attrib["v"]
        elif split_tokens[0] == "addr" and len(split_tokens) < 3:
            node = insert_address(node, split_tokens, tag)

    return node

# Fills in the 'refs' field for the node if the element is a 'way'
def get_refs(node, element):
    node["node_refs"] = []
    for ref in element.findall("nd"):
        node["node_refs"].append(ref.attrib["ref"])
        
    return node


def insert_address(node, address_name_tokens, tag):
    if "address" not in node:
        node["address"] = {}
    for token in address_name_tokens[1:]:
        if token == "street":
            node["address"][token] = audit.update_name(tag.attrib["v"], mapping)
        else:
            node["address"][token] = tag.attrib["v"]

    return node


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print "Not enough args"
    elif (len(sys.argv) > 2):
        print "Too many args"
    else:
        test(sys.argv[1])

