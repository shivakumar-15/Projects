#!/usr/bin/python

import os,sys,multiprocessing,json,time,re,Queue,glob,string
from time import sleep
from collections import Counter,defaultdict
#count = 0
#filetoopen = "./small-dataset.txt"
"""
try:
	filetoopen = "./"+str(sys.argv[2])
except IndexError:
	print "\n\n Enter the filename as the second parameter\n\n"
	exit()
"""
def filebound(n):
	
	""" Divides the file into chunks """

	filebounds = []
	filebounds.append(0)
	global filetoopen 
	fsize=os.path.getsize(filetoopen)
	#print fsize
	  
	#n = int(sys.argv[1])
	""" n is the number of threads """
	if fsize < 2000000:
		start = 500000/n
	elif fsize < 200000000:
		start = 2000000/n
	else:
		start = 100000000/n
	startptr = start
	#print "after dividing by %s %s" % (n,startptr)
	with open(filetoopen,"r") as robj:
		while True:
			robj.seek(startptr)
			while True:
				"""Checks for space after each work or EOF"""
                		if robj.read(1) == " " or robj.read(1) == "":
                			break
                		else:
                        		pass
                	filebounds.append(robj.tell())
                	#print "robj.tell() %s" % robj.tell()
                	startptr += start
			if startptr < fsize:
				pass
			else:
				endptr = fsize - robj.tell()
				filebounds.append(endptr+robj.tell())
				break	
                	#print "startptr %s" % startptr
                	#print "filebounds %s" % filebounds
	#print filebounds
	return filebounds,[(filebounds[i],filebounds[i+1]) for i in range(len(filebounds)-1)]

def filesplit(filecrop):

	""" Splits the one big file into smaller files """

	files = []
	with open(filetoopen,"r") as robj:
		for (sptr,eptr) in filecrop:
			data = robj.read(eptr - sptr)
			with open("./splitat%s.txt" %eptr, "w") as wobj:
				wobj.write(data)
				files.append(wobj.name)
	#print robj.closed, wobj.closed
	return files				
"""
def mergeresults(c1,i):
	print "thread#%s" % i
	merge = Counter()
	mergeresults.count += 1
	print mergeresults.count
	merge.update(c1)		
	print c1
	if mergeresults.count == n:
		print "INSIDE MERGE IF:"
		json.dump(merge,open("./merged.txt","w"),indent = 2)
	else:
		pass
"""
def fileallocate(filelist,n):
        #print filelist
        length = len(filelist)
        splitat = n*(length/n)
        print length,splitat
        filelist1 = filelist[:splitat]
        filelist2 = filelist[splitat:]
        print filelist1
        print filelist2
        print "\n\n"
        m = len(filelist1)/n # number of lists should be equal to no of threads
        print "M = %s" % m
        print "lenght of filelist %s" % len(filelist1)
        print "range(0,len(filelist1),m) %s" % range(0,len(filelist1),m)
        firstsplit = [filelist1[i:i+m] for i in range(0,len(filelist1),m)]
        print "LENGHT OF FIRSTSPLIT %s" % len(firstsplit)
        print "---------%s" % firstsplit
        #divider = len(firstsplit)
	divider = m
        print divider
        #finalist = [firstsplit[i % divider].append(filelist2[i]) for i in range(len(filelist2))]

        for i in range(len(filelist2)):
        #for i in range(8):
                insertat = i % divider
                print filelist2[i]
                firstsplit[insertat].append(filelist2[i])
                #firstsplit[insertat].append("XXXX")
                #firstsplit[insertat].append(filelist2[i])
                print "\n\n\n\n"
        print firstsplit
        print "LENGTH OF last FIRSTSPLIT %s" %len(firstsplit)
	return firstsplit

def filesort(filelist,X):

	""" Function to find the number of words in the chunks """
	for i in filelist:
                robj = open(i,"r")
                data = robj.read()
                pattern = re.compile(r"[a-z]+")
                sortedwords = pattern.findall(data)
                sortedwords.sort()
                #print sortedwords
                d = defaultdict(list)
                for i in sortedwords:
                        d[i[0]].append(i) 
                print d.values()
                for i in d.values():
                        a =[]
                        a.extend(i)
                        strings = "\n".join([i for i in a])
                        with open("./%s_%s_allwords.txt" % (a[0][0],X),"a") as wobj:
                                wobj.write(strings)

def similar_alpha_filemerge(alphalist,i):
	j = i	# The value of i changes in the nested for loop
	with open(r"./%s_all_merged_allwords.txt" % i,"a") as wobj:
		for i in alphalist:
			with open(i,"r") as robj:
				fdata = robj.read()
				wobj.write(fdata)
				fname = "%s_sorted_allwords.txt" % j
	filesort(["./%s_all_merged_allwords.txt" % j],fname)	#Using j here to open the same file 
"""
def mergedoutput(splitfiles):
        cnt = Counter()
        regex = re.compile(r"[\S]+:(?:\s[\d]+)+")
        for i in splitfiles:
                with open(i,"r") as robj:
                        data = robj.read()
                        keyvalue = re.findall(regex,data)
                        print keyvalue
                        counts = defaultdict(int)
                        for each in keyvalue:
                                word, count = each.split(': ')
                                word = word.strip('"')
                                counts[word] += int(count)


                        print counts
                        cnt.update(counts)
        json.dump(cnt,open("./mergedoutput.txt","w"), indent =2)


"""

if __name__ == "__main__":
	try:
                n = int(sys.argv[1])
        except IndexError:
                print "\n\nEnter the number of threads (2 to 8) as the first parameter\n\n"
                exit()
	try:
        	filetoopen = "./"+str(sys.argv[2])
	except IndexError:
        	print "\n\n Enter the filename as the second parameter\n\n"
        	exit()
	try:
		removefiles = glob.glob(r"./*allwords.txt")
		for i in removefiles:
			os.remove(i)
	except OSError:
		print "no files to delete"
        threads = []
	(filebounds,filecrop) = filebound(n)
	#print filecrop
	#print filebounds
	filelist = filesplit(filecrop)
	print filelist
	print "list length is %s" % len(filelist)
	firstsplit = fileallocate(filelist,n)
	merge = Counter()
	q = multiprocessing.Queue()
	for i in range(n):
		print firstsplit[i]
                t  = multiprocessing.Process(target = filesort,args= (firstsplit[i],i))
                #t2 = threading.Thread(target = wordcounter,args= (500000000,1000000000,"t2"))
                threads.append(t)
        st = time.time()
        for i in range(n):
                threads[i].start()
	
        for i in range(n):
                threads[i].join()
	print "\n\n\n\nTHREADS ARE JOINED\n\n\n\n"
        et = time.time()
	alphalist = list(string.ascii_lowercase)
	for i in alphalist:
		matchlist = glob.glob(r"./%s_[0-9]_allwords.txt" % i)
		similar_alpha_filemerge(matchlist,i)
	finallist = glob.glob("[a-z]_[a-z]_sorted_allwords.txt_allwords.txt")
	
	
	with open("./sort1MB-sharedmemory_allwords.txt","a") as wrobj:
		for i in finallist:
			with open(i,"r") as rrobj:
				data = rrobj.read()
				#data1 = " ".join(data)
				wrobj.write(data)
		
	#queuelist =  [q.get() for i in range(n)]		
	#mergedoutput(queuelist)
        totaltime = et - st
        print totaltime 

	"""
	starttime = time.time()
	wordcount(filelist)			
	endtime = time.time()
	totaltime = endtime - starttime
	print "totaltime =  %s" % totaltime
	"""
