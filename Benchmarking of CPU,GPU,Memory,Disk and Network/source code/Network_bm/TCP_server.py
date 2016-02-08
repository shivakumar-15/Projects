#!/usr/bin/python

from socket import  *
from time import *
import os,sys
#fobj = open(r"D:\shiva\movies\The Wire Season 1\Read Me.txt","r")
host=""
port=1914
#bufsize=os.path.getsize(r"D:\shiva\movies\The Wire Season 1\Read Me.txt")
addr=(host,port)
bsize = int(sys.argv[1])
svrsck = socket(AF_INET,SOCK_STREAM)
svrsck.bind(addr)
svrsck.listen(5)
while True:
	print "waiting for connection......"
	childsck,addr=svrsck.accept()
	print "accepted conn from",addr
	while True:
		data=childsck.recv(bsize)
		if not data:
			break
		#rspn="[%s]--%s" % (ctime(),data)
		rspn="%s" % (data)
		childsck.send(rspn)
	childsck.close()
		#print data
svrsck.close()
	
