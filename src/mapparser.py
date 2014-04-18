#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module does the iterative parsing to process the map file and
identifies the unique tags that are present and also counts how many 
occurrences are there for each tag.
The output is a dictionary with the tag name as the key
and number of times this tag was encountered in the map as value.
"""

import xml.etree.ElementTree as ET
import pprint
import sys

def count_tags(filename):
    data = {}
    for event, elem in ET.iterparse(filename):
        if elem.tag in data:
            data[elem.tag] += 1
        else:
            data[elem.tag] = 1
    return data

def test():
    if len(sys.argv) != 2:
        print("Usage: " + sys.argv[0] + " <file name to be processed>")
        exit(1)

    tags = count_tags(sys.argv[1])
    pprint.pprint(tags)  

if __name__ == "__main__":
    test()