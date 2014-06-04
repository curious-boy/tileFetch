#coding: utf-8
#! /usr/bin/env python
#filename: getUrlPicFromRange.py

#introduction: download pic file from a range ,between idstart and idend,
# and record the undownload file in qrcodelist.txt

import os,sys,string,time
from getTile import *


#url_prefix url
# idstart 
# idend
# format  png /jpg  
def downUrlPic(url_prefix, idstart,idend, format,dstdir):
	if url_prefix == "":
		return;
	url_pic = "";
	#print url_pic

	qrcodefile = "qrcodelist.txt"

	#process child thread exception
	listecp = []

	try:
		file_object = open(qrcodefile, 'w')

		for curid in xrange(idstart,idend):
			url_pic = url_prefix + str(curid) + "." + format;
			print "url_pic: %s" % url_pic
		

			try:
				#print "-----------------------1----------"
				filesize = getTileEx(listecp, url_pic,dstdir + str(curid) + "." + format  )
				print "filesize: %s" % filesize
				if int(filesize) > 20000 :
					print "file: %s.%s is not exist..." % (curid, format)
					file_object.writelines(url_pic + "\n")
					#file_object.writeline
					#print "--------------"
				else:
					#print "file: %s.%s is exist..." % (curid, format)
					print "%s was download..."  % url_pic
					file_object.writelines(url_pic+"\n")
				#os.getcwd()
			except Exception, e:
				file_object.close();
				print "\ngetTileEx exception happen"	
				raise GetPicException( str(curid))
		file_object.close()
		
	except GetPicException, e1:
		file_object.close()
		print e1
		print e1.name		
		# store name of undownload file  to file
	except Exception , e:
		file_object.close()
		print e
		sys.exit()

	


if __name__ == '__main__':
	url_prefix = "http://union.mchina.cn/images/digitalcode/" 
	idstart= 15900;
	idend=16600
	format = "png"
	dstdir = os.getcwd() + "\\pic_range\\" 
	#print "dstdir: %s" % dstdir

	downUrlPic(url_prefix, idstart, idend, format, dstdir )
