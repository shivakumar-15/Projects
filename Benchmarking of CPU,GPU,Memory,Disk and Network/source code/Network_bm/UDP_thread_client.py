#!/usr/bin/python

#!/usr/bin/python
from socket import *
import os,threading,sys
from time import *


fobj = open(r"./1MB.txt","r")
fsize=os.path.getsize(r"./1MB.txt")
port=[1916,1917]
bsize = int(sys.argv[1])
length = len(port)
threads = []
def client_socket(portno,bsize):
	clisck=socket(AF_INET,SOCK_DGRAM)
	host="localhost"
	addr=(host,portno)
	totaltime = 0.0
	while True:
		data=fobj.read(bsize)
		if not data:
			break                       
 		starttime = clock()
		clisck.sendto(data,addr)
		resp,addr = clisck.recvfrom(bsize)
        	endtime= clock() - starttime
		totaltime += endtime
        	#print resp,
        	#print starttime, endtime
        	#print "totaltime within loop:"+str(endtime)
		#timetaken = float(endtime) - float(starttime)
        	#totaltime += timetaken
        	#print float(bufsize)
        	#speed = float(bufsize)/float(tt)
        	#print speed
	clisck.close()
	#print "totaltime:"+str(totaltime)
	#print "File size:"+str(fsize)+" Bytes"
	bw = float(fsize)/float(totaltime)
	#print "Bandwidth:"+str((bw))
	print "\nBandwidth:"+str(bw/1000000)+" Mbytes/sec\n\n"

def main():
	for i in port:
		udpclient = threading.Thread(target = client_socket , args = (i,bsize))
		threads.append(udpclient)
	for i in range(length):
		threads[i].start()
if __name__ == "__main__":
	main()
