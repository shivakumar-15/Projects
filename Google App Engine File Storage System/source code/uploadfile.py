#! /usr/bin/env python
import cloudstorage as gcs	
import os,cgi,re
import urllib
import webapp2


from google.appengine.api import memcache
from google.appengine.api import app_identity
from google.appengine.api import files
from google.appengine.ext import db
import google.appengine.ext.blobstore as BS
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import webapp

class MainHandler(webapp.RequestHandler):
	def get(self):
		self.response.out.write('<html><head>')
		self.response.out.write("For Files more than 32 MB")
		self.response.out.write("""
					<script>
					function myfun(){
					var filname = document.getElementById("lfile").value; 
					var newstring = String(filname);
					var fname = newstring.substring(12);
					var arr1 = arr[arr.length - 1];
					document.getElementById("fileID").value = newstring;
					}
					</script>
					</head>	
					<form action="http://storage.googleapis.com/cloudstoragepa04.appspot.com" method="post" enctype="multipart/form-data">
					<input type="text" id = "fileID" name="key" />
					<input type="hidden" name="success_action_redirect" value="http://cloudstoragepa04.appspot.com/">
					<input name="file" id="lfile" type="file">
					<input type="submit" value="Upload Large Files"> 
					</form>""")
		self.response.out.write('<form action="/upload" method="POST" enctype="multipart/form-data">')
    		self.response.out.write("""InsertFile less than 32 MB: <input type="file" name="files" multiple/><br> <input type="submit" name="submit" value="Insert File"> </form>""")
		self.response.write('<form action="/check" method="post">')
                self.response.write("""Check File: <input type="text" name="cfile"><br> <input type="submit" name="submit" value="Check"> </form>""")
    		self.response.write('<form action="/find" method="post">')
    		self.response.write("""Find File: <input type="text" name="nfile"><br> <input type="submit" name="submit" value="Find"> </form>""")
		self.response.write('<form action="/delete" method="post">')
		self.response.write("""Remove File: <textarea name="dfile" cols="40" rows="5"></textarea><br> <input type="submit" name="submit" value="Delete"> </form>""")
		self.response.write('<form action="/removeallcache" method="post">')
 		self.response.write('<input type="submit" name="submit" value="Remove All Cache"> </form>')
		self.response.write('<form action="/deleteall" method="post">')
 		self.response.write('<input type="submit" name="submit" value="Remove All"> </form>')
		self.response.write('<form action="/cachesize" method="post">')
		self.response.write('<input type="submit" name="submit" value="Cache size"> </form>')
		self.response.write('<form action="/cachesizeelem" method="post">')
 		self.response.write('<input type="submit" name="submit" value="Cache elements"> </form>')
		self.response.write('<form action="/listall" method="post">')
		self.response.write('<input type="submit" name="submit" value="List All"> </form>')
		self.response.write('<form action="/regexlistall" method="post">')
		self.response.write('Regex File All: <input type="text" name="rlafile"><br>')
 		self.response.write('<input type="submit" name="submit" value="Regex List All"> </form>')
		self.response.write('<form action="/matchregex" method="post">')
 		self.response.write('Find In File: <input type="text" name="mregx"><br>')
 		self.response.write('<input type="submit" name="submit" value="Find in file"> </form>')
		self.response.write('<form action="/storagesizeelem" method="post">')
                self.response.write('<input type="submit" name="submit" value="StorageSizeElem"> </form>')
		self.response.write('<form action="/storagesizemb" method="post">')
                self.response.write('<input type="submit" name="submit" value="StorageSizeMB"> </form>')
    		self.response.write('</body></html>')

class UploadHandler(webapp.RequestHandler):
  
	def post(self):
    		fileslist = self.request.POST.getall('files')
		length = len(fileslist)
		print fileslist	
    		for i in fileslist:
			j = i
			print i,j
			print i.filename
			data = j.file.read()
			size = i.file.tell()
			fileName = bucketName + '/' + i.filename 
			self.response.out.write(fileName)
			if size <= 100000:
				memcache.add(i.filename,data)
			uploadFile = gcs.open(fileName,'w',content_type='text/plain')
    			uploadFile.write(data)
    			uploadFile.close()
		rvalue = "%s Files uploaded successfully" % length
		self.response.out.write("""
                                        <script type = "text/javascript">
                                        function myfunc()
                                        {
                                        alert(document.getElementById("checkmem").value);
                                        window.location.href = '/';
                                        }
                                        </script></head>""")
                self.response.out.write('<body onload = myfunc()>')
                self.response.out.write('<input type = "hidden" id = "checkmem" value = "%s">' % rvalue)
		#self.redirect('/')

class FindHandler(webapp2.RequestHandler):

	def post(self):
		
		fileToFind = cgi.escape(self.request.get('nfile'))
		fileName = bucketName + '/' + fileToFind
		memData = memcache.get(fileToFind)
		if memData is not None:
			headerType = "attachment; filename = %s" % fileToFind
			self.response.headers['Content-Disposition'] = str(headerType)
			self.response.write(memData)
			self.response.write("From memcache file %s" % fileToFind)
		else:
			self.response.out.write("%s %s\n" % (fileToFind,fileName))
			fileDownLoad = gcs.open(fileName)
			headerType = "attachment; filename = %s" % fileToFind
			self.response.headers['Content-Disposition'] = str(headerType)
			self.response.write(fileDownLoad.read())
			self.response.write("From GCS file %s" % fileToFind)

		

class CheckHandler(webapp2.RequestHandler):

	def post(self):

		fileToCheck = cgi.escape(self.request.get('cfile'))
		data = memcache.get(fileToCheck)
		if data is not None:
			rvalue = "File: %s present in memcache" % fileToCheck 
			self.response.out.write("""
                                        <script type = "text/javascript">
                                        function myfunc()
                                        {
                                        alert(document.getElementById("checkmem").value);
                                        window.location.href = '/';
                                        }
                                        </script></head>""")
			self.response.out.write('<body onload = myfunc()>')
                        self.response.out.write('<input type = "hidden" id = "checkmem" value = "%s">' % rvalue)

			
		else:
			fileToChecknGs = '/gs%s/%s' % (bucketName,fileToCheck)
			fileList = files.listdir("/gs%s" % bucketName)
			print fileToChecknGs,fileList
			if fileToChecknGs in fileList:
				rvalue = "File: %s in present in GCS" %fileToCheck
				self.response.out.write("""
                                        <script type = "text/javascript">
                                        function myfunc()
                                        {
                                        alert(document.getElementById("checkmem").value);
                                        window.location.href = '/';
                                        }
                                        </script></head>""")
			        self.response.out.write('<body onload = myfunc()>')
                        	self.response.out.write('<input type = "hidden" id = "checkmem" value = "%s">' % rvalue)
			else:
				rvalue = "File: %s is not present in memcache and  GCS" % fileToCheck
				self.response.out.write("""
                                        <script type = "text/javascript">
                                        function myfunc()
                                        {
                                        alert(document.getElementById("check").value);
                                        window.location.href = '/';
                                        }
                                        </script></head>""")
                                self.response.out.write('<body onload = myfunc()>')
                                self.response.out.write('<input type = "hidden" id = "check" value = "%s">' % rvalue)

class ListAllHandler(webapp2.RequestHandler):
	def post(self):
		self.response.out.write(files.listdir("/gs%s" % bucketName))

class StorageSizeMB(webapp2.RequestHandler):

	def post(self):
                f = gcs.listbucket(bucketName)
                sz = 0
                for i in f:
                        sz += i.st_size
		sizeinMB = float(sz)/1000000
		rvalue = "The GCS file storage size is %s MB" % sizeinMB
		self.response.out.write("""
                                        <script type = "text/javascript">
                                        function myfunc()
                                        {
                                        alert(document.getElementById("StorageSize").value);
                                        window.location.href = '/';
                                        }
                                        </script></head>""")
                self.response.out.write('<body onload = myfunc()>')
                self.response.out.write('<input type = "hidden" id = "StorageSize" value = "%s">' % rvalue)

class StorageSizeElem(webapp2.RequestHandler):


	def post(self):
		length = len(files.listdir("/gs%s" % bucketName))
		rvalue = "Number of Files in GCS is %s" % length
		self.response.out.write("""
                                        <script type = "text/javascript">
                                        function myfunc()
                                        {
                                        alert(document.getElementById("Storedelems").value);
                                        window.location.href = '/';
                                        }
                                        </script></head>""")
                self.response.out.write('<body onload = myfunc()>')
                self.response.out.write('<input type = "hidden" id = "Storedelems" value = "%s">' % rvalue)

class RemoveAllCacheHandler(webapp2.RequestHandler):

	def post(self):
		rvalue = memcache.flush_all()
		self.response.out.write('<html><head>')
		self.response.out.write("""
					<script type = "text/javascript">
					function myfunc()
					{
					alert(document.getElementById("mem2").value);
					window.location.href = '/';
					}
					</script></head>""")
		self.response.out.write('<body onload = myfunc()>')
		self.response.out.write('<input type = "hidden" id = "mem2" value = "%s">' % rvalue)
	        self.response.out.write('</body></html>')
		#self.redirect('/')
class DeleteAllHandler(webapp2.RequestHandler):

	def post(self):
		memcache.flush_all()
		rvalue = files.delete(*files.listdir("/gs%s" % bucketName))
		self.response.out.write("""
                                        <script type = "text/javascript">
                                        function myfunc()
                                        {
                                        alert(document.getElementById("deleteall").value);
                                        window.location.href = '/';
                                        }
                                        </script></head>""")
                self.response.out.write('<body onload = myfunc()>')
                self.response.out.write('<input type = "hidden" id = "deleteall" value = "True">')


class DeleteHandler(webapp2.RequestHandler):

	def  post(self):
		self.response.out.write("in delete")
		self.response.out.write(bucketName)
		bucKet = gcs.listbucket(bucketName)
		fileListFromBkt =[i.filename for i in bucKet]
		print fileListFromBkt
		deleteFiles = self.request.POST.getall('dfile')
		print deleteFiles
		#deleteFiles.split()
		#deleteFiles = for i in deleteFiles:
		#deleteFiles = deleteFiles.split()
		for i in deleteFiles:
			j = bucketName+'/'+i
			if j in fileListFromBkt:
				gcs.delete(j)
				rvalue = "DELETED FILE %s" % j
                		self.response.out.write("""
                                        <script type = "text/javascript">
                                        function myfunc()
                                        {
                                        alert(document.getElementById("delete").value);
                                        window.location.href = '/';
                                        }
                                        </script></head>""")
                		self.response.out.write('<body onload = myfunc()>')
                		self.response.out.write('<input type = "hidden" id = "delete" value = "%s">' % rvalue)
			else:	
				rvalue = "not present %s" % j
				self.response.out.write("""
                                        <script type = "text/javascript">
                                        function myfunc()
                                        {
                                        alert(document.getElementById("delete").value);
                                        window.location.href = '/';
                                        }
                                        </script></head>""")
                                self.response.out.write('<body onload = myfunc()>')
                                self.response.out.write('<input type = "hidden" id = "delete" value = "%s">' % rvalue)

class CacheSizeHandler(webapp2.RequestHandler):

	def post(self):
		memDict = memcache.get_stats()
		memSize = float(memDict['bytes']) / 1000000
		rvalue = "Mem size is %s MB" % memSize
                self.response.out.write("""
                                        <script type = "text/javascript">
                                        function myfunc()
                                        {
                                        alert(document.getElementById("memcacheSize").value);
                                        window.location.href = '/';
                                        }
                                        </script></head>""")
                self.response.out.write('<body onload = myfunc()>')
                self.response.out.write('<input type = "hidden" id = "memcacheSize" value = "%s">' % rvalue)
		
class CacheSizeElemHandler(webapp2.RequestHandler):

	def post(self):
		memDict = memcache.get_stats()
		memFiles = memDict['items'] - 1
		rvalue = "Number of file in memCache is %s" % memFiles
		self.response.out.write("""
                                        <script type = "text/javascript">
                                        function myfunc()
                                        {
                                        alert(document.getElementById("memcacheElems").value);
                                        window.location.href = '/';
                                        }
                                        </script></head>""")
                self.response.out.write('<body onload = myfunc()>')
                self.response.out.write('<input type = "hidden" id = "memcacheElems" value = "%s">' % rvalue)

class RegexListAll(webapp2.RequestHandler):

	def post(self):
		regexp = cgi.escape(self.request.get('rlafile'))
		#flist = re.findall(regexp,
		#self.response.out.write(regexp)
	        f = gcs.listbucket(bucketName)
		filesInBucket = " ".join([i.filename[13:] for i in f])
		matchInBucket = re.findall(r'\w*%s\w*' % regexp,filesInBucket)
		rvalue = "The matched files for the pattern is %s" % matchInBucket
		self.response.out.write("""
                                        <script type = "text/javascript">
                                        function myfunc()
                                        {
                                        alert(document.getElementById("regexlistall").value);
                                        window.location.href = '/';
                                        }
                                        </script></head>""")
                self.response.out.write('<body onload = myfunc()>')
                self.response.out.write('<input type = "hidden" id = "regexlistall" value = "%s">' % rvalue)

class BmFindHandler(webapp2.RequestHandler):

	def post(self,resource):
	
		fileToFind = cgi.escape(self.request.get('nfile'))
                fileName = bucketName + '/' + fileToFind
                self.response.out.write("%s %s\n" % (fileToFind,fileName))
		memData = memcache.get(fileToFind)
		if memData is not None:
 			self.response.write(memData)
			self.response.write("From memcache file %s" % fileToFind)
		else:   
 			self.response.out.write("%s %s\n" % (fileToFind,fileName))
 			fileDownLoad = gcs.open(fileName)
			self.response.write(fileDownLoad.read())
			self.response.write("From GCS file %s" % fileToFind)
	
	def get(self,resource):
                fileToFind = resource[1:]
		print fileToFind
		fileName = bucketName + '/' + fileToFind
                self.response.out.write("%s %s\n" % (fileToFind,fileName))
                memData = memcache.get(fileToFind)
                if memData is not None:
                        self.response.write(memData)
                        self.response.write("From memcache file %s" % fileToFind)
                else:
                        self.response.out.write("%s %s\n" % (fileToFind,fileName))
                        fileDownLoad = gcs.open(fileName)
                        self.response.write(fileDownLoad.read())
                        self.response.write("From memcache file %s" % fileToFind)


class MatchRegex(webapp2.RequestHandler):

	def post(self):
		
		f = gcs.listbucket(bucketName)
		filesInBucket = [i.filename[13:] for i in f]
		stringBucket = " ".join(filesInBucket)
		pattern = cgi.escape(self.request.get('mregx'))
	        match = re.search('\w*%s\w*' % pattern,stringBucket)	
		if match:
			#rvalue = "pattern is %s true for %s" % (pattern,match.group(0))
			rvalue = "True"
			self.response.out.write("""
                                        <script type = "text/javascript">
                                        function myfunc()
                                        {
                                        alert(document.getElementById("regex").value);
                                        window.location.href = '/';
                                        }
                                        </script></head>""")
                	self.response.out.write('<body onload = myfunc()>')
                	self.response.out.write('<input type = "hidden" id = "regex" value = "%s">' % rvalue)
			
		else:
			#rvalue ="False pattern %s does not match any file"  % (pattern,match.group(0))
			rvalue = "False"
			self.response.out.write("""
                                        <script type = "text/javascript">
                                        function myfunc()
                                        {
                                        alert(document.getElementById("regex").value);
                                        window.location.href = '/';
                                        }
                                        </script></head>""")
                	self.response.out.write('<body onload = myfunc()>')
                	self.response.out.write('<input type = "hidden" id = "regex" value = "%s">' % rvalue)

bucketDefault = os.environ.get('BUCKET_NAME',app_identity.get_default_gcs_bucket_name())	
#bucketName = '/pa03bucket1'
bucketName ='/'+bucketDefault

app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/upload', UploadHandler),
			       ('/find', FindHandler),
			       ('/check', CheckHandler),
			       ('/delete', DeleteHandler),
			       ('/bmfind(.*)', BmFindHandler),
			       ('/listall', ListAllHandler),
			       ('/removeallcache', RemoveAllCacheHandler),
			       ('/deleteall', DeleteAllHandler),
			       ('/cachesize', CacheSizeHandler),
			       ('/cachesizeelem', CacheSizeElemHandler),
			       ('/regexlistall', RegexListAll),
			       ('/matchregex', MatchRegex),
			       ('/storagesizeelem', StorageSizeElem),
			       ('/storagesizemb', StorageSizeMB)],
                               debug=True)

