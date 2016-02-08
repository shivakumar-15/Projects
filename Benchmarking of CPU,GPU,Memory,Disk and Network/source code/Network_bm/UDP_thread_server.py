#!/usr/bin/python

from socket import  *
from time import *
import os,sys,threading
port = [1916,1917]
length = len(port)
threads = []
bsize = int(sys.argv[1])
def server_socket(portno,bsize):
	host=""
	addr=(host,portno)

	svrsck = socket(AF_INET,SOCK_DGRAM)
	svrsck.bind(addr)
	#svrsck.listen(5)
	while True:
		print "waiting for connection......"
		#childsck,addr=svrsck.accept()
		#print "accepted conn from",addr
		while True:
			data,addr=svrsck.recvfrom(bsize)
			if not data:
				break
			#rspn="[%s]--%s" % (ctime(),data)
			#rspn="%s" % (data)
			svrsck.sendto(data,addr)
			#print data
	svrsck.close()

def main():
	for i in port:
		udpserverthr = threading.Thread(target = server_socket , args = (i,bsize))
		threads.append(udpserverthr)
	for i in range(length):
		threads[i].start()

if __name__ == "__main__":
	main()
