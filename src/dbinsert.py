#!/usr/bin/env python

import json
import sys

def insert_data(data, db):

# Insert the data into a collection 'OpenStreetMap.newdelhi'
# read the json file and insert the data into MongoDB
#
    db.OpenStreetMap.newdelhi.insert(data)

if __name__ == "__main__":
 
    if len(sys.argv) != 2:
        print("Usage: " + sys.argv[0] + " <file name to be processed>")
        exit(1)
		
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    db = client.examples

    with open(sys.argv[1]) as f:
        data = json.loads(f.read())
        insert_data(data, db)
        print(db.OpenStreetMap.newdelhi.find_one())