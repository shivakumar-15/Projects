#!/usr/bin/python
import time,os,threading,random,sys
def fileread(fsize,rsize):
	#with open("/Users/chaithanyaanichettymurali/Documents/Masters/networking/3MB.txt","r") as fobj:
	with open("./1MB.txt","r") as fobj:
		#robj = open("/Users/chaithanyaanichettymurali/Documents/Masters/networking/W1MB.txt","r")
		robj = open("./3MB.txt","r")
		#print "fileread"
		totaltime = 0
		for i in xrange(1,2000):
			ttfbr = 0
			while True:
				rdata = robj.read(rsize)
				if not rdata:
					break
				randacc=random.randint(1,fsize)
                		starttime = time.time()
				fobj.seek(randacc)
                		fobj.read(rsize)
                		endtime = time.time() - starttime
				#print "latency %s" % endtime
				ttfbr += endtime
        		#print " for %sth time taken is %s " %(i,ttfbr)
			#print "file tell :%s" % robj.tell()
			robj.seek(0)
        		fobj.seek(0)
        		totaltime += ttfbr
		robj.close()
	operation = "read"
	bandwidthcal(totaltime,operation)	
def filewrite(fsize,rsize):
        fsize=os.path.getsize("/Users/chaithanyaanichettymurali/Documents/Masters/networking/W1MB.txt")
	fsize=os.path.getsize("./W1MB.txt")
        #print "filewrite"
        totaltime = 0
        for i in xrange(1,2000):
                #with open("/Users/chaithanyaanichettymurali/Documents/Masters/networking/1MB.txt","r") as wrobj:
		with open("./3MB.txt","r") as wrobj:
                        ttfbw = 0
                        #fname = "/Users/chaithanyaanichettymurali/Documents/Masters/networking/3MB.txt"
			fname = "./sample.txt"
                        wobj = open(fname,"w")
                        while True:
                                text = wrobj.read(rsize)
                                if not text:
                                        break
                                randomacc = random.randint(1,fsize)
				starttime = time.time()
                                wobj.seek(randomacc)
                                wobj.write(text+"\n")
                                endtime = time.time() - starttime
				#print "latency %s" % endtime
                                ttfbw += endtime
                        wobj.close()
                        totaltime += ttfbw
        operation = "write"
        bandwidthcal(totaltime,operation)

#def filewrite2(fsize):
#	with open(r"/Users/chaithanyaanichettymurali/Documents/Masters/networking/samplewrite.txt","w") as wobj:
def bandwidthcal(totaltime,operation):
        #fsize=os.path.getsize("/Users/chaithanyaanichettymurali/Documents/Masters/networking/1MB.txt")
	fsize=os.path.getsize("./1MB.txt")
        #print "filesize= %s" %fsize
        bandwidth = (fsize*2000)/(1000000*totaltime)
	print "%s bandwidth is %s Mbyte/sec" % (operation,bandwidth)
#wobj = open(r"/Users/chaithanyaanichettymurali/Documents/Masters/networking/samplewrite.txt","a")
def main():
	#print "inside main"
	#fsize=os.path.getsize("/Users/chaithanyaanichettymurali/Documents/Masters/networking/1MB.txt")
	fsize=os.path.getsize("./1MB.txt")
	rsize = int(sys.argv[1])
	fileread(fsize,rsize)
	filewrite(fsize,rsize)
if __name__ == "__main__":
	main()
