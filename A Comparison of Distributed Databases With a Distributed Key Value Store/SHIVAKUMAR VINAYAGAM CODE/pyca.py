from cassandra.cluster import Cluster

import datetime
import random
peers={}            #this lists the static peer which are there and their ips and ports
noofpeers=0
clients=[]
dht=[]

def readpeers():
    infile = open("config1.txt",'r')
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
	cluster = Cluster([peer["Serverip"]])
	session = cluster.connect('test')
        #client=MongoClient("mongodb://"+peer["Serverip"]+":"+peer["Serverport"])
        clients.append(session)


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
        session=clients[sel]
        session.execute("insert into dht (key,value) values ('"+str(dht[i])+"','"+value+"')")
        #db.test.insert_one({str(dht[i]):value})
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
        session=clients[sel]
        result = session.execute("select * from dht where key='"+str(dht[i])+"'")
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
        session=clients[sel]
        result = session.execute("delete from dht where key='"+str(dht[i])+"'")
    etime=datetime.datetime.now()
    diff=etime-stime
    print diff
    avg=diff.total_seconds()/10000
    print "avg time taken to delete 10000 entries",avg


noofpeers=readpeers()
createclients()

print clients
print peers
benchmark()




'''
cluster = Cluster()
session = cluster.connect('test')
#session.execute("update users set age = 36 where lastname = 'Jones'")
session.execute("insert into dht (key,value) values ('"+str(12453)+"','"+"sample"+"')")
result = session.execute("select * from dht")
print result
for res in result:
	print res.key,res.value
result = session.execute("select * from dht where key='"+str(12453)+"'")
for res in result:
        print res.key,res.value
'''
