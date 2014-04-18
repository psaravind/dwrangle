#!/usr/bin/env python

def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

def make_pipeline():
    # complete the aggregation pipeline
    pipeline = [ { "$project" : { "timestamp" : "$created.timestamp"}},                
                 { "$sort" : { "timestamp" : 1}},
                 { "$limit" : 10 }]
    return pipeline

def aggregate(db, pipeline):
    result = db.OpenStreetMap.chennai.aggregate(pipeline)
    return result

if __name__ == '__main__':
    db = get_db('examples')
    pipeline = make_pipeline()
    result = aggregate(db, pipeline)
    import pprint
    pprint.pprint(result["result"])