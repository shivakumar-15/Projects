#!/usr/bin/python           # This is client.py file
import sys
import socket               # Import socket module
import cPickle as pickle
from os import listdir
from os.path import isfile, join
import threading
import datetime
import time 
from pprint import pprint
import random

#this peer
peerip="0.0.0.0"
peerport=1214

testcase="True"     #True for client program to send 100000 requests or false for the user input interface
duplicates="False"   #True for maintaining 1 duplicate of each key/value pair across the whole dht
dht={}		    #This is the Local distributed hash table
peers={}            #this lists the static peer which are there and their ips and ports
noofpeers=0

prevdht={}
dupdht={}
class PeerServerThread(threading.Thread):

    def __init__(self,ip,port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        print "[+] New thread started for "+ip+":"+str(port)

    def run(self):    
        print "Connection from : "+self.ip+":"+str(self.port)
        #clientsock.send("\nWelcome to the server\n\n")
        data = clientsock.recv(2048)
        print "Client sent : "+data
        if len(data):
            undat= pickle.loads(data) #data loaded
            print undat
            if undat['method']=="putentry":
                print "put entry method was called for key",undat['key']
                dht[undat['key']]=undat['value']
                clientsock.send("ack")
                clientsock.shutdown(socket.SHUT_WR)
            if undat['method']=="deleteentry":
                print "delete entry method was called for key",undat['key']
                if undat['key'] in dht:
                    del dht[undat['key']]
                    clientsock.send("ack")
                else:
                    clientsock.send("entry not present")
                clientsock.shutdown(socket.SHUT_WR)
            if undat['method']=="getentry":
                print "get entry method was called for key",undat['key']
                if undat['key'] in dht:
                    value=dht[undat['key']]
                else:
                    value="null"
                clientsock.send(value)
                clientsock.shutdown(socket.SHUT_WR)
            if undat['method']=="duplicate":
                print "duplicate method was called for key",undat['key']
                dupdht[undat['key']]=undat['value']
                clientsock.send("ack")
                clientsock.shutdown(socket.SHUT_WR)
        print "Client disconnected..."

def selectpeer(key):
    inter=hash(key)
    sel=inter%noofpeers
    #print sel
    peer=peers[sel]
    #print peer
    #print key
    return peer

def selectnextpeer(key):
    inter=hash(key)
    sel=inter%noofpeers
    #print sel
    sel=(sel+1)%noofpeers
    peer=peers[sel]
    #print peer
    #print key
    return peer

def sendmsg(peer,msg):
    server=socket.socket()
    server.connect((peer["Serverip"],int(peer["Serverport"])))
    senddata=pickle.dumps(msg,-1)
    server.send(senddata)
    print "sending msg dict to corresponding peer"
    resp=server.recv(2048)
    server.close()
    return resp
    
    

def addentry(key,value):
    peer=selectpeer(key)
    msg={}
    msg["method"]="putentry"
    msg["key"]=key
    msg["value"]=value
    result=sendmsg(peer,msg)
    if result=="ack":
        print "Value added to local dht in",peer
    else:
        print "Failure in adding value to dht" 


def deleteentry(key):
    peer=selectpeer(key)
    msg={}
    msg["method"]="deleteentry"
    msg["key"]=key
    result=sendmsg(peer,msg)
    if result=="ack":
        print "Value was deleted from local dht in",peer
    else:
        print "Failure in deleting value- entry not present"


def getentry(key):
    peer=selectpeer(key)
    msg={}
    msg["method"]="getentry"
    msg["key"]=key
    result=sendmsg(peer,msg)
    if len(result):
    	return result 

def duplicate(key,value):
    peer=selectnextpeer(key)
    msg={}
    msg["method"]="duplicate"
    msg["key"]=key
    msg["value"]=value
    result=sendmsg(peer,msg)
    if result=="ack":
        print "Value duplicated to local dht in",peer
        return "ack"
    else:
        print "Failure in adding value to dht"
    

def resilience():
    print "resilience was set to true, so starting duplication"
    while(True):
        print "resilience thread sleeping for 60sec"
        time.sleep(60)
        print "resilience process starts"
        for key,value in dht.items():
            if key not in prevdht:
                print "duplicating key",key
                res=duplicate(key,value)
                if res=="ack":
                    prevdht[key]=value
        
   


def clientuserio():
    print "This is the client user interface"
    ch=1
    while(ch<5):
        print "\n 1.Addentry 2.deleteentry 3.getvalue 4.print local-dht  anything else to exit"
        ch=int(raw_input("enter your choice:"))
        if ch==1:
            key=int(raw_input("enter the key:"))
            value=raw_input("enter the value:")
            addentry(key,value)
        if ch==2:
            key=int(raw_input("enter the key:"))
            deleteentry(key)
        if ch==3:
            key=int(raw_input("enter the key:"))
            value=getentry(key)
            if value=="null":
                print "The key was not present in DHT"
            else:
                print "The value for that key is",value
        if ch==4:
            pprint(dht)            
    print "exiting User interface"


def peerclientthread():
    
    print "The test case was set to true so starting testing for evaluation thread if u need user-io put false as 3rd argument"
    #inp=raw_input("start calculate avg time for 100000 registers")
    time.sleep(10)
    stime=datetime.datetime.now()
    for i in range(10000,20000):
        addentry(i,str(i))
    etime=datetime.datetime.now()
    diff=etime-stime
    avg=diff.total_seconds()/10000
    print "avg time taken to add 10000 entries",avg
    f = open("res"+str(random.random()),'wb+')
    s=str(diff)+"avg time taken to add 10000 entries"+str(avg)+"\n"
    f.write(s)
    
    stime=datetime.datetime.now()
    for i in range(10000,20000):
        getentry(i)
    etime=datetime.datetime.now()
    diff=etime-stime
    avg=diff.total_seconds()/10000
    print "avg time taken to get 10000 entries",avg
    s=str(diff)+"avg time taken to get 10000 entries "+str(avg)+"\n"
    f.write(s)
    
    stime=datetime.datetime.now()
    for i in range(10000,20000):
        deleteentry(i)
    etime=datetime.datetime.now()
    diff=etime-stime
    avg=diff.total_seconds()/10000
    print "avg time taken to delete 10000 entries",avg
    s=str(diff)+"avg time taken to delete 10000 entries "+str(avg)+"\n"
    f.write(s)
    f.close()
    

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


if __name__ == '__main__':
    noofpeers=readpeers()
    print peers
    print "The no of static peers are",noofpeers
    try:
        print "Start the program with - python peer#.py peerip peerport testcase(True or False) resilience(True or False)"
        if len(sys.argv)>4:
            args=str(sys.argv)
            print args
            peerip=sys.argv[1]
            peerport=int(sys.argv[2])
            testcase=sys.argv[3]
            duplicate=sys.argv[4]
            
        tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print "this peer is listening at",peerip,peerport
        tcpsock.bind((peerip,peerport))
        threads = []
        
        if testcase=="True":
            thread = threading.Thread(target=peerclientthread, args=())
            thread.daemon = True                            # Daemonize thread
            thread.start()
        else:
            thread = threading.Thread(target=clientuserio, args=())
            thread.daemon = True                            # Daemonize thread
            thread.start()
        if duplicates=="True":
            thread = threading.Thread(target=resilience, args=())
            thread.daemon = True                            # Daemonize thread
            thread.start()

        while True:
            tcpsock.listen(4)
            print "\nListening for incoming connections..."
            (clientsock, (inip, inport)) = tcpsock.accept()
            newthread = PeerServerThread(inip, inport)
            newthread.start()
            threads.append(newthread)
        
        for t in threads:
            t.join()

    except Exception, e:
        print >> sys.stderr, str(e)
	sys.exit(1)
    sys.exit(0)
