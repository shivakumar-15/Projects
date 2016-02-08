#! /usr/bin/env python

import requests
import os,time
from multiprocessing import Process


def upload(filelist):

	for i in filelist:
	
		f = {}
		f = {'files':open("/Users/chaithanyaanichettymurali/Documents/Masters/gaefiles/%s" % i, "rb")}
		print "uploading %s" % i
		r = requests.post('http://cloudstoragepa04.appspot.com/upload', files = f)	

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
	starttime = time.time()
	upload(filelist)
	endtime = time.time()
	totaltime = endtime - starttime
	print "totaltime : %s" % totaltime
