#!/usr/bin/env python

import pprint
import sys
    
def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

def make_pipeline(p):
# aggregation pipeline
    if p == 0:
        print("Query top users, count of entries created, min and max dates")
        pipeline = [ { "$group" : {"_id" : "$created.user", 
                                   "count" : { "$sum" : 1 }, 
                                   "min" : {"$min" : "$created.timestamp"},
                                   "max" : {"$max" : "$created.timestamp"}} },                
                     { "$sort" : { "count" : -1}},
                     { "$limit" : 10 }]
    elif p == 1:
        print("Query earliest entry timestamp")
        pipeline = [ { "$project" : { "timestamp" : "$created.timestamp"}},                
                     { "$sort" : { "timestamp" : 1}},
                     { "$limit" : 1 }]
    elif p == 2:
        print("Query latest entry timestamp")       
        pipeline = [ { "$project" : { "timestamp" : "$created.timestamp"}},                
                     { "$sort" : { "timestamp" : -1}},
                     { "$limit" : 1 }]                   
    elif p == 3:
        print("Query count of entries by Year and Month, sorted by count")
        pipeline = [ { "$project" : { "datetime" : { "$substr": ["$created.timestamp", 0, 7 ]}}},
                     { "$group" : {"_id" : "$datetime",          
                                   "count" : { "$sum" : 1 }}},
                     { "$sort" : { "count" : -1}}]  
    elif p == 4:
        print("Query count of entries by Year and Month, sorted by Year/Month")
        pipeline = [ { "$project" : { "datetime" : { "$substr": ["$created.timestamp", 0, 7 ]}}},
                     { "$group" : {"_id" : "$datetime",          
                                   "count" : { "$sum" : 1 }}},
                     { "$sort" : { "_id" : 1}}]     
    elif p == 5:
        print("Query count of Place of Worship")
        pipeline = [ { "$project" : { "amenity" : { "$eq" : ["$amenity", "place_of_worship" ]},
                                      "religion" : "$religion" }},
                     { "$group" : { "_id" : "$religion",
                                    "count" : { "$sum" : 1 }}},
                     { "$sort" : { "count" : 1}}]                                   
    elif p == 6:
        print("Query count of different Amenities")
        pipeline = [ { "$project" : { "amenity" : "$amenity" }},
                     { "$group" : { "_id" : "$amenity",
                                    "count" : { "$sum" : 1 }}},
                     { "$sort" : { "count" : 1}}]
    elif p == 7:
        print("Query count of different places of tourism")
        pipeline = [ { "$project" : { "tourism" : "$tourism" }},
                     { "$group" : { "_id" : "$tourism",
                                    "count" : { "$sum" : 1 }}},
                     { "$sort" : { "count" : 1}}]
    return pipeline

def aggregate(db, pipeline):
    result = db.OpenStreetMap.newdelhi.aggregate(pipeline)
    return result

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: " + sys.argv[0] + " <query # to process>")
        exit(1)
        
    db = get_db('examples')
    pipeline = make_pipeline(int(sys.argv[1]))
    result = aggregate(db, pipeline)

    pprint.pprint(result["result"])