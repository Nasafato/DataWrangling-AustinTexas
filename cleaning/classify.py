import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
import sys

OSMFILE = ""

def parse():
    classifications = process(OSMFILE)
    pprint.pprint(dict(dict(classifications)))

def process(osmfile):
    osm_file = open(osmfile)
    classifications = defaultdict(dict) 
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            classify_tags(elem, classifications)
        
    return classifications

def classify_tags(elem, classifications):
    for tag in elem.iter("tag"):
        key = tag.attrib["k"]
        if key in classifications:
            classifications[key]["count"] += 1
            classifications[key]["items"].add(tag.attrib["v"])
        else:
            classifications[key]["count"] = 1
            classifications[key]["items"] = set([tag.attrib["v"]])

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print "Not enough args"
    elif (len(sys.argv) > 2):
        print "Too many args"
    else:
        OSMFILE = sys.argv[1]
        parse()
