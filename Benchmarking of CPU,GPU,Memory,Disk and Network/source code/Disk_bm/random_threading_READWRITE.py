#!/usr/bin/python
import time,os,threading,random,sys
def fileread(fsize,rsize):							#Function to read file
	with open("/Users/chaithanyaanichettymurali/Documents/Masters/networking/1MB.txt","r") as fobj:
		robj = open("/Users/chaithanyaanichettymurali/Documents/Masters/networking/W1MB.txt","r")
	#	print "fileread"
		totaltime = 0
		for i in xrange(1,2000):
			ttffr = 0					#variable to cal total time for file read
			while fobj.tell() < fsize:
				randacc=random.randint(1,fsize)
                		starttime = time.time()
				fobj.seek(randacc)
                		fobj.read(rsize)
                		endtime = time.time() - starttime
				ttffr += endtime			#total time taken to read the file once
				#print "READ `LATENCY: %s"% endtime
			robj.seek(0)
			fobj.seek(0)
			totaltime += ttffr
        		#print " for %sth time taken is %s " %(i,ttffr)
			#print "file tell :%s" % fobj.tell()
			#print "totaltime %s" % totaltime
			
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
                        #wobj = open("/Users/chaithanyaanichettymurali/Documents/Masters/misc/samplewrite.txt","w")
                        while True:
                                text = fobj.read(rsize)
                                if not text:
                                        break
				randomacc = random.randint(1,fsize)
                                starttime = time.time()
				wobj.seek(randomacc)
                                wobj.write(text+"\n")
                                endtime = time.time() - starttime
                                ttfbw += endtime
			#	print "LATENCY %s" % endtime
                        #wobj.close()
			#print " time for %s time is %s	" % ( i , ttfbw)
                        totaltime += ttfbw
        operation = "write"
        bandwidthcal(totaltime,fsize,operation)

def bandwidthcal(totaltime,fsize,operation):
	print "Totaltime is %s" % totaltime
        #print "filesize= %s" %fsize
        throughput = (fsize*2000)/(1000*totaltime)
	print "%s throughput is %s Kbytes/sec" % (operation,throughput)
wobj = open("/Users/chaithanyaanichettymurali/Documents/Masters/misc/samplewrite.txt","w")
def main():
        #print "inside main"
        fsize=os.path.getsize("/Users/chaithanyaanichettymurali/Documents/Masters/networking/1MB.txt")
	rsize = int(sys.argv[1])
	n = int(sys.argv[2])
	if n < 2:
		print " Please enter number of threads - 2 or 4 ? "
		exit()
	threads = []
        for i in range(n-1):
                readthr = threading.Thread(target = fileread,args=(fsize,rsize))
                writethr = threading.Thread(target = filewrite,args=(fsize,rsize))
                threads.extend([readthr,writethr])
        for i in range(n):
                threads[i].start()
        for i in range(n):
                threads[i].join()
	wobj.close()
if __name__ == "__main__":
        main()

