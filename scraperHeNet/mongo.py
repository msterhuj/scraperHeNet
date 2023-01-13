import pymongo

client = pymongo.MongoClient('172.16.1.22', 27017)
db = client['interdex']
