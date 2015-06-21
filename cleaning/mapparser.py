#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
The output should be a dictionary with the tag name as the key
and number of times this tag can be encountered in the map as value.

Note that your code will be tested with a different data file than the 'example.osm'
"""
import xml.etree.ElementTree as ET
import pprint
import sys

def count_tags(filename):
    tag_dict = {}
    iterator = ET.iterparse(filename)
    for entry in iterator:
        tag = entry[1].tag
        if tag in tag_dict:
            tag_dict[tag] += 1
        else:
            tag_dict[tag] = 1
    return tag_dict
            
def parse(filename):
    tags = count_tags(filename)
    pprint.pprint(tags)
                         

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Not enough args"
    else:
        parse(sys.argv[1])
