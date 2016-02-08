#!/usr/bin/python

from socket import  *
from time import *
import os,threading,sys
port=[1914,1915]
bsize = int(sys.argv[1])
length = len(port)
threads=[]
def server_socket(portno,bsize):
	host=""
	addr=(host,portno)

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
def main():
	for i in range(length):
		svrthr = threading.Thread(target = server_socket, args = (port[i],bsize))
		threads.append(svrthr)
	for i in range(length):
		threads[i].start()
if __name__ == "__main__":
	main()
