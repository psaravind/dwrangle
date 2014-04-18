#!/usr/bin/env python

"""
This module does following two steps:

- audit the OSMFILE and the variable 'mapping' reflects the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    4 new entries "Salai", "Nagar", "Extension", "Marg" were added, these names
    are local vernacular names that refer to street/road/place.
- update_name function actually fixes the street name.
    The function takes a string with street name as an argument and returns the fixed name
"""

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import sys

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Salai", "Nagar", "Extension", "Marg", "Avenue", 
            "Boulevard", "Drive", "Court", "Place", "Square", "Lane", 
            "Road", "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE
mapping = { r' [sS]t\b': " Street",
            r' [rR]d\b': " Road",
            r' [aA]ve\b': " Avenue",
            r' [eE]xtn\b': " Extension"
            }

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit(osmfile):
    osm_file = open(osmfile, "r", encoding="utf8")
    street_types = defaultdict(set)

    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types

def update_name(name, mapping):
    for s in mapping.keys():
        p = re.compile(s)	
        if p.search(name):
            name = p.sub(mapping[s], name)
            return name

    return name

def test():
    if len(sys.argv) != 2:
        print("Usage: " + sys.argv[0] + " <file name to be processed>")
        exit(1)

    st_types = audit(sys.argv[1])
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.items():
        for name in ways:
            better_name = update_name(name, mapping)
            print(name, "=>", better_name)

if __name__ == '__main__':
    test()