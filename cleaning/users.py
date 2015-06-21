#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
import sys
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""

def get_user(element):
    return element.attrib['uid']

def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if element.tag == 'node':
            users.add(get_user(element))
        
    return users

def parse(filename):
    users = process_map(filename)
    pprint.pprint(users)
    pprint.pprint(len(users))

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print "Not enough args"
    elif (len(sys.argv) > 2):
        print "Too many args"
    else:
        test(sys.argv[1])
    
