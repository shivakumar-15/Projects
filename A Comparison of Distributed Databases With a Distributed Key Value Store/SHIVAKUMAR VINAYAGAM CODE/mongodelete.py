from pymongo import MongoClient

client1=MongoClient()
db1 = client1.test
db1.test.insert_one({"x":2})
print "db1 count",db1.test.count()
