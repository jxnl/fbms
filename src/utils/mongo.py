import pymongo import MongoClient

client = Mongoclient("mongodb://marksweep:pennapps@ds035300.mongolab.com:35300/marksweep")
db = client['marksweep']
logs = db['logs']
logs.insert(t)




