#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import pprint
import re
import sys

"""
This module explores the data a bit more and finds out how many unique users
have contributed to map this particular area!

The function process_map returns a set of unique user IDs ("uid")
"""

def get_user(element):
    return

def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if 'uid' in element.attrib:
            users.add(element.attrib['uid'])

    return users

def test():
    if len(sys.argv) != 2:
        print("Usage: " + sys.argv[0] + " <file name to be processed>")
        exit(1)

    users = process_map(sys.argv[1])
    pprint.pprint(users)
    print("Unique user count:", len(users))

if __name__ == "__main__":
    test()