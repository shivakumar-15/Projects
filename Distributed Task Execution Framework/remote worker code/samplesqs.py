#!/usr/bin/python  

import os,json
import boto.sqs
import boto.dynamodb
#from boto.sqs.message import Message
from time import sleep
from boto.sqs.message import RawMessage

reqQ = boto.sqs.connect_to_region('us-east-1').create_queue('MyQueue1')
respQ = boto.sqs.connect_to_region('us-east-1').create_queue('respQueue')
respQ.set_message_class(RawMessage)
ddb = boto.dynamodb.connect_to_region('us-east-1')

ddb_Schema = ddb.create_schema(
        hash_key_name='jobid',
        hash_key_proto_value=str
    )
try:
	ddb_Table = ddb.create_table(
			name = 'messages',
			schema = ddb_Schema,
			read_units=10,
        		write_units=10
			)
except boto.exception.DynamoDBResponseError:
	ddb_Table = ddb.get_table('messages')

print "tables in the db %s" % ddb.list_tables()
m = RawMessage()
print "length of the Queue %s" % reqQ.count()
while True:
	resp = {}
	print "inside While"
	Qmsg = reqQ.get_messages()#message_attributes=['first'])
	print len(Qmsg)
        if len(Qmsg) > 0:
		print "Q count %d" % reqQ.count()
                #Qmsg = reqQ.get_messages()
                #mesg =  Qmsg[0].get_body()
		data = json.loads(Qmsg[0].get_body())
		jobid = data['jobid'][0]
		cid   = data['clientid'][0]
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
			try:
				exec task
				resp['jobdesc'] = "%s task executed successfully" % jobid
				resp['jobid']   = jobid
				resp['clientid']= cid
				m.set_body(json.dumps(resp))
				#text = json.dumps("success")
				#m.set_body("success")
				respQ.write(m)
				reqQ.delete_message(Qmsg[0])
		
			except:
				resp['jobdesc'] = "%s task executed failed" % jobid
                                resp['jobid']   = jobid
                                resp['clientid']= cid
				m.set_body(json.dumps(resp))
				respQ.write(m)
			#reqQ.delete_message(Qmsg[0])
		"""
                m.set_body(mesg)
                respQ.write(m)
		reqQ.delete_message(Qmsg[0])
		"""
        else:
		print "inside parent else"
		timer = 0
		for i in range(10):
			print "inside parent else queue size is %d" % reqQ.count()
			if reqQ.count() > 0:
				break
			else:
				timer += 1
				print "timer is %d" % timer
				print "%s sleeping for 2 seconds" % i
				print "count is %d" % reqQ.count()
				sleep(2)
				if timer == 10:
					print "value of i is %s" % i
					print "shutdown"
					exit(0)

print "exited succesfully"
