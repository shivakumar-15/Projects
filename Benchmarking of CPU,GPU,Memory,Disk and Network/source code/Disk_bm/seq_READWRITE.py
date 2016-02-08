#!/usr/bin/python
import time,os,threading,random,sys
def fileread(fsize,rsize):							#Function to read file
	with open("/Users/chaithanyaanichettymurali/Documents/Masters/networking/1MB.txt","r") as fobj:
		#print "fileread"
		totaltime = 0
		for i in xrange(1,2000):
			ttffr = 0					#variable to cal total time for file read
			while True:
                		starttime = time.time()
                		data = fobj.read(rsize)
                		endtime = time.time() - starttime
				ttffr += endtime			#total time taken to read the file once
				if not data:
					break
				print "READ `LATENCY: %s"% endtime
        		#print " for %sth time taken is %s " %(i,ttffr)
			#print "file tell :%s" % fobj.tell()
			#print "totaltime %s" % totaltime
			totaltime += ttffr
	operation = "Read"
	bandwidthcal(totaltime,fsize,operation)	
	#print "FILE POINTER: %s "% fobj
def filewrite(fsize,rsize):
        #print "filewrite"
        totaltime = 0
        for i in xrange(1,2000):
                with open("/Users/chaithanyaanichettymurali/Documents/Masters/networking/W1MB.txt","r") as fobj:
                        ttfbw = 0
                        #fname = "/Users/chaithanyaanichettymurali/Documents/Masters/misc/samplewrite"+str(i)+".txt"
                        wobj = open("/Users/chaithanyaanichettymurali/Documents/Masters/misc/samplewrite.txt","w")
                        while True:
                                text = fobj.read(rsize)
                                if not text:
                                        break
                                starttime = time.time()
                                wobj.write(text+"\n")
                                endtime = time.time() - starttime
                                ttfbw += endtime
				#print "LATENCY %s" % endtime
                        wobj.close()
                        totaltime += ttfbw
        operation = "write"
        bandwidthcal(totaltime,fsize,operation)

def bandwidthcal(totaltime,fsize,operation):
	print "Totaltime is %s" % totaltime
        #print "filesize= %s" %fsize
        throughput = (fsize*2000)/(1000*totaltime)
	print "%s throughput is %s Kbytes/sec" % (operation,throughput)
def main():
        #print "inside main"
        fsize=os.path.getsize("/Users/chaithanyaanichettymurali/Documents/Masters/networking/1MB.txt")
	rsize = int(sys.argv[1])
	if rsize == " ":
		print "Enter the record size"
		exit()
	fileread(fsize,rsize)
	filewrite(fsize,rsize)
if __name__ == "__main__":
        main()


