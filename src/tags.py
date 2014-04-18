#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import pprint
import re
import sys

"""
This module explores the data a bit more.
Before we process the data and add it into MongoDB, we should
check the "k" value for each "<tag>" and see if they can be valid keys in 
MongoDB, as well as see if there are any other potential problems.

We use 3 regular expressions to check for certain patterns
in the tags. We change the data model and expand the "addr:street" type of 
keys to a dictionary like : {"address": {"street": "Some value"}}
"""

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    if element.tag == "tag":
        if lower.match(element.attrib['k']):
            keys['lower'] += 1
        elif lower_colon.match(element.attrib['k']):
            keys['lower_colon'] += 1
        elif problemchars.match(element.attrib['k']):
            keys['problechars'] += 1
        else:
            keys['other'] += 1
            
    return keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

def test():
    if len(sys.argv) != 2:
        print("Usage: " + sys.argv[0] + " <file name to be processed>")
        exit(1)

    keys = process_map(sys.argv[1])
    pprint.pprint(keys)

if __name__ == "__main__":
    test()