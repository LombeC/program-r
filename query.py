from pymongo import MongoClient

# A MongoDB instance for Python
mongo_client = MongoClient('mongodb://ryanrobotics.com:27017/')

db = mongo_client.programr
col = db.conversations

query = {"image" : { "filename" : "This_is_the_default", "duration" : None } }
result = col.find(  )

for x in result:
    print(x)