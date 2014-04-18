#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json
import sys

"""
This module wrangles the data and transform the shape of the data
into the model that is suitable for data analysis. The output is a list of dictionaries
that look like this:
	{
		"pos": [28.5514681, 77.2954887], 
		"id": "367288184", 
		"created": {
			"timestamp": "2009-11-01T19:49:52Z", 
			"uid": "42123", 
			"version": "2", 
			"changeset": "3010394", 
			"user": "Ropino"
		}, 
		"address": {
			"street": "Abul Fazal Road", 
			"housenumber": "M-91", 
			"city": "New Delhi", 
			"postcode": "110025"
		}, 
		"type": "node"
	}
The shape_element function parses the map file, and calls the function with the element
as an argument. Function returns a dictionary, containing the shaped data for that element.
After process the data, process_map saves the data in a file, so that the file could be used
for mongoimport to import the shaped data into MongoDB. This module does not do any
cleaning, only shapes the structure.

In particular the following things are done:
- process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" turned into regular key/value pairs, except:
    - attributes in the CREATED array added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing.  Values inside "pos" array are floats. 
- if second level tag "k" value contains problematic characters, they are ignored
- if second level tag "k" value starts with "addr:", they are added to a dictionary "address"
- if second level tag "k" value does not start with "addr:", but contains ":", they the tag
-     is processed same as any other tag.
- if there is a second ":" that separates the type/direction of a street,
  the tag is ignored.
"""

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        node['id'] = element.attrib['id']
        node['type'] = element.tag
        if 'visible' in element.attrib:
            node['visible'] = element.attrib['visible']
        node['created'] = {}
        for c in CREATED:
            node['created'][c] = element.attrib[c]
        if 'lat' in element.attrib:
            node['pos'] = [float(element.attrib['lat']), float(element.attrib['lon'])]
        if element.find("tag") != None:
            #node['address'] = {}
            for tag in element.iter("tag"):
                if lower_colon.match(tag.attrib['k']) and tag.attrib['k'].startswith("addr:"):
                    if 'address' not in node:
                        node['address'] = {}
                    node['address'][tag.attrib['k'].split(":")[1]] = tag.attrib['v']
                elif lower.match(tag.attrib['k']) and not tag.attrib['k'].startswith("addr:"):
                    node[tag.attrib['k']] = tag.attrib['v']
        if element.find("nd") != None:
            node["node_refs"] = []
            for nd in element.iter("nd"):
                node["node_refs"].append(nd.attrib['ref'])
            
        return node
    else:
        return None

def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    for _, element in ET.iterparse(file_in):
        el = shape_element(element)
        if el:
            data.append(el)
    
    with open(file_out, "w") as f:
        f.write("[\n")
        i = 0
        for item in data:
            i += 1
            if i == 1:
                f.write(json.dumps(item))
            else:
                f.write(",\n" + json.dumps(item))
        f.write("\n]")

    return data

def test():
    if len(sys.argv) != 2:
        print("Usage: " + sys.argv[0] + " <file name to be processed>")
        exit(1)
		
    data = process_map(sys.argv[1], True)
    #pprint.pprint(data)

if __name__ == "__main__":
    test()