#coding: utf-8
#! /usr/bin/env python
#filename: getUrlPicFromList.py

#introduction: read line from qrcodelist.txt, download pic ,and record the file un download

import os,sys,string,time
from getTile import *

def downUrlPicFromList(rfile,wfile, dstdir):
	#process child thread exception
	listecp = []

	try:
		file_read = open(rfile, 'r')
		#global file_write
		file_write = open(wfile, 'w')

		while 1:
			url_pic = file_read.readline();
			url_pic = url_pic.strip('\n')
			#print "url_pic: %s" % url_pic
			if not url_pic:
				break

			split_code="/"
			#slist = url_pic[url_pic.find(split_code)+5:]
			#slist = url_pic[url_pic.find(split_code[, 1][, 5])]
			#print( url_pic.split('/')[5].split('\\')[0])
			#print slist

			try:

				filesize = getTileEx(listecp, url_pic,dstdir + url_pic.split('/')[5] )
				print "filesize: %s" % filesize

				if int(filesize) > 20000 :
					print "file: %s is not exist..." % url_pic
					file_write.writelines(url_pic + "\n")
					#print "-----------------------3----------"
				else:
					print "%s was download..."  % url_pic
					#file_w.writeline(url_pic)
				#os.getcwd()
			except Exception, e:
				file_read.close();
				file_write.close()
				print "\ngetTileEx exception happen"	
				raise GetPicException( url_pic)
		print "file was closed"
		file_read.close()
		file_write.close()
		
	except GetPicException, e1:
		file_read.close()
		file_write.close()
		print e1
		print e1.name
		#print "dddddddd"
		# store name of undownload file  to file
	except Exception , e:
		file_read.close()
		file_write.close()
		print e
		sys.exit()

	


if __name__ == '__main__':
	listfile = os.getcwd() + "\\" + "qrcodelist.txt"
	writefile = os.getcwd() + "\\" + "qrcodelist_bak.txt"
	dstdir = os.getcwd() + "\\pic_list\\" 
	#print "dstdir: %s" % dstdir
	#print writefile

	downUrlPicFromList( listfile , writefile, dstdir )

	#print "rename"
	os.remove( listfile )
	os.rename(writefile, listfile)