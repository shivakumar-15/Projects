#! /usr/bin/env python

import requests
import os,time
from multiprocessing import Process


def upload(filelist):

	for i in filelist:
	
		f = {}
		f = {'files':open("/Users/chaithanyaanichettymurali/Documents/Masters/gaefiles/%s" % i, "rb")}
		print "uploading %s" % i
		r = requests.post('http://cloudstoragepa04.appspot.com/upload', files = f, data = d)	

def search(filelist):

	
        for i in filelist:
		print i
		d = { 'nfile':'%s' % i }
		print d
		r = requests.post('http://cloudstoragepa04.appspot.com/bmfind', data = d)
		data = r.text
		wdata = open("/Users/chaithanyaanichettymurali/Documents/Masters/Cloud_Computing/PA3/fromgcs/%s" % i , "w")
		wdata.write(data)
		wdata.close()

def delete(filelist):

	for i in filelist:
		d = { 'dfile':'%s' % i }
		r = requests.post('http://cloudstoragepa04.appspot.com/delete', data = d)
		print r.text		


if __name__ == "__main__":

	filelist = os.listdir("/Users/chaithanyaanichettymurali/Documents/Masters/gaefiles")
	#filelist.extend(os.listdir("/Users/chaithanyaanichettymurali/Documents/Masters/gaefiles"))
	print filelist
	d = {'enctype':'multipart/form-data'}
	length = len(filelist)
	splitat = 4*(length/4)
        print length,splitat
        filelist1 = filelist[:splitat]
        filelist2 = filelist[splitat:]
	print filelist1,filelist2
	m = len(filelist1)/4
	print "M = %s" % m
        print "lenght of filelist %s" % len(filelist1)
        print "range(0,len(filelist1),m) %s" % range(0,len(filelist1),m)
        firstsplit = [filelist1[i:i+m] for i in range(0,len(filelist1),m)]
        print "LENGHT OF FIRSTSPLIT %s" % len(firstsplit)
        print "---------%s" % firstsplit
        #divider = len(firstsplit)
        divider = 4
        print divider
	#print finalist
	for i in range(len(filelist2)):
                insertat = i 
                print filelist2[i]
                firstsplit[insertat].append(filelist2[i])
                #firstsplit[insertat].append("XXXX")
                #firstsplit[insertat].append(filelist2[i])
                print "\n\n\n\n"
        print firstsplit
	process = []
	for i in firstsplit:
		p = Process(target = search, args = (i,))
		process.append(p)
	starttime = time.time()
	for i in process:
		i.start()
	for i in process:
		i.join()
	endtime = time.time()
	totaltime = endtime - starttime
	print "totaltime %s" % totaltime
