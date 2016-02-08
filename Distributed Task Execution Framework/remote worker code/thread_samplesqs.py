#!/usr/bin/python  

import os,json
import boto.sqs
import boto.dynamodb
from boto.sqs.message import RawMessage
from time import sleep,time
from multiprocessing import Process 


reqQ = boto.sqs.connect_to_region('us-east-1').create_queue('MyQueue1')
respQ = boto.sqs.connect_to_region('us-east-1').create_queue('respQueue')
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

def workers(j):
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
			cid = data['clientid'][0]
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
				job_id = data['jobid'][0]
				task = data['jobdesc'][0]
				print data
				try:
					exec task
					resp['jobdesc'] = "%s task with jobid:%s executed successfully" %(task,job_id)
					resp['jobid'] = job_id
					resp['clientid'] = cid
					print resp
					m.set_body(json.dumps(resp))
					respQ.write(m)
					reqQ.delete_message(Qmsg[0])
				except:
					resp = "%s task with jobid:%s failed" %(task,job_id)
					m.set_body(json.dumps(resp))
					respQ.write(m)
				"""
				exec task
                                resp['jobdesc'] = "%s task with jobid:%s executed successfully" %(task,job_id)
                                resp['jobid'] = job_id
                                resp['clientid'] = cid
				print resp
                                m.set_body(json.dumps(resp))
                                respQ.write(m)
                                reqQ.delete_message(Qmsg[0])
				"""
		else:
			print "inside parent else"
			timer = 0
			for i in range(10):
				print "inside parent else queue size is %d" % reqQ.count()
				#if reqQ.count() > 0:
				length = reqQ.get_messages()
				if len(length) > 0:
					break
				else:
					timer += 1
					print "timer is %d" % timer
					print "Process %s is sleeping for 2 seconds and iter is %s" % (j,i)
					print "count is %d" % reqQ.count()
					sleep(2)
					if timer == 10:
						print "value of i is %s" % i
						print "shutdown"
						exit(0)

if __name__ == "__main__":
	proc_list = []
	for i in range(4):
		p = Process(target = workers, args = (i,))
		proc_list.append(p)
	start_time = time()
	for i in proc_list:
		i.start()
	for i in proc_list:
		i.join()
	end_time = time()
	total_time = end_time - start_time
	print "total time is %s" % total_time

