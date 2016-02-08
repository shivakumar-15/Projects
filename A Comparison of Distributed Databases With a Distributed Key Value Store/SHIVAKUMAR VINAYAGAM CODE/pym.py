from pymongo import MongoClient
import datetime
import random
peers={}            #this lists the static peer which are there and their ips and ports
noofpeers=0
clients=[]
dht=[]

def readpeers():
    infile = open("config.txt",'r')
    firstline = infile.readline()
    fields=firstline.split("\t")
    fields.remove("\n")
    #print fields
    lines= infile.readlines()
    z=0
    for i in lines:
        values=[]
        values=i.split("\t")
        values.remove("\n")
        x=0
        repo={}
        while x<len(fields):
            repo[fields[x]]=values[x]
            x+=1
        peers[z]=repo
        z+=1
    return z

def selectpeer(key):
    inter=hash(key)
    sel=inter%noofpeers
    #print sel
    #peer=peers[sel]
    #print peer
    #print key
    return sel


def createclients():
    for i,peer in peers.items():
        client=MongoClient("mongodb://"+peer["Serverip"]+":"+peer["Serverport"])
        clients.append(client)


def benchmark():
    for i in range(1,10001):
        dht.append(int(random.random()*(10**10)))
    print len(dht)
    print dht[9999]
    stime=datetime.datetime.now()
    for i in range(0,10000):
        value=''.join(str(dht[i]) for i in range(1,10))
        #print len(value)
        #print value
        sel=selectpeer(dht[i])
        client=clients[sel]
        db=client.test
        db.test.insert_one({str(dht[i]):value})
    etime=datetime.datetime.now()  
    diff=etime-stime
    print diff
    avg=diff.total_seconds()/10000
    print "avg time taken to add 10000 entries",avg
    

    stime=datetime.datetime.now()
    for i in range(0,10000):
        value=''.join(str(dht[i]) for i in range(1,10))
        #print len(value)
        #print value
        sel=selectpeer(dht[i])
        client=clients[sel]
        db=client.test
        cursor=db.test.find({str(dht[i]):value})
        
    etime=datetime.datetime.now()
    diff=etime-stime
    print diff
    avg=diff.total_seconds()/10000
    print "avg time taken to get 10000 entries",avg
    
    stime=datetime.datetime.now()
    for i in range(0,10000):
        value=''.join(str(dht[i]) for i in range(1,10))
        #print len(value)
        #print value
        sel=selectpeer(dht[i])
        client=clients[sel]
        db=client.test
        result = db.test.delete_many({str(dht[i]):value})
    etime=datetime.datetime.now()
    diff=etime-stime
    print diff
    avg=diff.total_seconds()/10000
    print "avg time taken to delete 10000 entries",avg
    


'''db = client.test
#db.test.insert_one({"x":2})
print db.test.count()
cursor = db.test.find()
for document in cursor:
    print(document)'''

noofpeers=readpeers()
createclients()

print clients
print peers
benchmark()



'''client = MongoClient()
db = client.test
#db.test.insert_one({"x":2})
print db.test.count()
cursor = db.test.find()
for document in cursor:
    print(document)

client1=MongoClient("mongodb://172.31.43.168:27017")
db1 = client1.test
db1.test.insert_one({"x":2})
print "db1 count",db1.test.count()

noofpeers=readpeers()
print readpeers'''
