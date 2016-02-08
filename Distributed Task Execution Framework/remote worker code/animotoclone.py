#!/usr/bin/python  

import os,json
import boto.sqs
import boto.dynamodb
from boto.sqs.message import RawMessage
from time import sleep
import time
import requests
from boto.s3.connection import S3Connection
from boto.s3.connection import Location
from boto.s3.key import Key
import boto

reqQ = boto.sqs.connect_to_region('us-east-1').create_queue('url')
respQ = boto.sqs.connect_to_region('us-east-1').create_queue('url_response')
ddb = boto.dynamodb.connect_to_region('us-east-1')
resp = {}
ddb_Schema = ddb.create_schema(
        hash_key_name='jobid',
        hash_key_proto_value=str
    )
try:
	ddb_Table = ddb.create_table(
			name = 'urls',
			schema = ddb_Schema,
			read_units=10,
        		write_units=10
			)
except boto.exception.DynamoDBResponseError:
	ddb_Table = ddb.get_table('urls')

print "tables in the db %s" % ddb_Table
m = RawMessage()
print "length of the Queue %s" % reqQ.count()
j = 1
timer = 0
starttime = time.time()
while True:
	print "inside While"
	Qmsg = reqQ.get_messages()#message_attributes=['first'])
	print len(Qmsg)
        if len(Qmsg) > 0:
		print "Q count %d" % reqQ.count()
                #Qmsg = reqQ.get_messages()
                #mesg =  Qmsg[0].get_body()
		data = json.loads(Qmsg[0].get_body())
		jobid = data['jobid'][0]
		try:
			item_Get = ddb_Table.get_item( hash_key =  jobid )
			print "try"
			print "item_Get %s" % item_Get
			pass
		except boto.dynamodb.exceptions.DynamoDBKeyNotFoundError:
			print "inside except"
			item_data = { 'jobdesc':data['jobdesc'][0] }
			item = ddb_Table.new_item( hash_key = jobid,
					    attrs = item_data)
			item.put()	
			task = data['jobdesc'][0]
			print data
			with open(r'/home/ubuntu/images/img%d.jpg' % j , 'wb') as wobj:
                		r = requests.get(task, stream = True)
                		wobj.write(r.content)
                	print r.status_code
			reqQ.delete_message(Qmsg[0])
			j += 1   
        else:
		print "inside parent else"
		#for i in range(10):
		if reqQ.count() > 0:
			pass
		else:
			timer += 1
			print "timer is %d" % timer
			print " sleeping for 2 seconds"
			print "count is %d" % reqQ.count()
			sleep(1)
			if timer == 10:
				print "shutdown"
				break

os.system("ffmpeg -y -framerate 1/1  -i /home/ubuntu/images/img%d.jpg -b:v 3000000 /tmp/video1.mp4")

s3_conn = S3Connection()
try:
        bucket = s3_conn.get_bucket('chaithu')
except boto.exception.S3CreateError:
        bucket = s3_conn.create_bucket('chaithu',location=Location.USWest)
#print '\n'.join(i for i in dir(Location) if i[0].isupper())
k = Key(bucket)
k.key = 'video1'
meta_d = bucket.lookup('video1')
k.set_contents_from_filename('/tmp/video1.mp4')
k.get_contents_to_filename('/home/ubuntu/images/yourvideo.mp4')
url = k.generate_url(expires_in=0, query_auth=False)
k.set_acl('public-read')
print bucket,url
resp['jobdesc'] = url
m.set_body(json.dumps(resp))
respQ.write(m)
endtime = time.time()
timetaken = endtime - starttime
print "timetake is %s" % timetaken


