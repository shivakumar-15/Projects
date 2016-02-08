#!/usr/bin/python

#!/usr/bin/python
from socket import *
import os,sys
from time import *


fobj = open(r"./1MB.txt","r")
fsize=os.path.getsize(r"./1MB.txt")
#fsize=os.path.getsize(r"/Users/chaithanyaanichettymurali/Desktop/resume.textClipping")
clisck=socket(AF_INET,SOCK_DGRAM)
host="localhost"
port=1916
addr=(host,port)
#clisck.connect(addr)
totaltime = 0.0
bsize = int(sys.argv[1])

while True:
	data=fobj.read(bsize)
	if not data:
		break                       
 	starttime = clock()
	clisck.sendto(data,addr)
	resp,addr = clisck.recvfrom(bsize)
        endtime= clock() - starttime
	#print "latency %s" % endtime
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
print "Bandwidth:"+str((bw/1000000))+" Mbtyes/sec"
