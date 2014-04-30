#coding: utf-8
#!/usr/bin/env python
#filename: getTile.py 

import StringIO
import pycurl

class GetTileExcption(Exception):
	"""下载切片异常处理"""
	def __init__(self, identifier,row, col, num):
		super(GetTileExcption, self).__init__()
		self.identifier = identifier
		self.row = row
		self.col = col
		self.num = num

# down tile and save file
def getTile(url, filename ):

	try:
		#f = open(xfilename, "w")
		html = StringIO.StringIO()
		c = pycurl.Curl()
		
		c.setopt(pycurl.URL, url)

		#c.setopt(pycurl.PROXY, "http://10.1.3.164:8083")
		c.setopt(pycurl.HTTPPROXYTUNNEL,1) 
		c.setopt(pycurl.NOSIGNAL, 1)

		# callback
		c.setopt(pycurl.WRITEFUNCTION, html.write)
		c.setopt(pycurl.FOLLOWLOCATION, 1)

		# max times of relocation
		c.setopt(pycurl.MAXREDIRS, 5)

		c.setopt(pycurl.CONNECTTIMEOUT, 60)
		c.setopt(pycurl.TIMEOUT, 30)

		c.setopt(pycurl.USERAGENT, "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)")

		c.perform()

		f = open("%s" % (filename,), 'wb')
		f.write(html.getvalue())
		f.close()
	except Exception, e:
		print e
	
	
# down tile and save file
def getTileEx(listecp,url, filename ):

	try:
		#f = open(xfilename, "w")
		html = StringIO.StringIO()
		c = pycurl.Curl()
		
		c.setopt(pycurl.URL, url)

		c.setopt(pycurl.PROXY, "http://10.1.3.164:8083")
		c.setopt(pycurl.HTTPPROXYTUNNEL,1) 
		c.setopt(pycurl.NOSIGNAL, 1)

		# callback
		c.setopt(pycurl.WRITEFUNCTION, html.write)
		c.setopt(pycurl.FOLLOWLOCATION, 1)

		# max times of relocation
		c.setopt(pycurl.MAXREDIRS, 5)

		c.setopt(pycurl.CONNECTTIMEOUT, 60)
		c.setopt(pycurl.TIMEOUT, 30)

		c.setopt(pycurl.USERAGENT, "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)")

		c.perform()

		f = open("%s" % (filename,), 'wb')
		f.write(html.getvalue())
		f.close()
	except Exception, e:
		listecp.append("exceptiontag")		



		