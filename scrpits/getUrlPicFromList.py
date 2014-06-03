#coding: utf-8
#! /usr/bin/env python
#filename: getUrlPicFromList.py

import os,sys,string,time
from getTile import *

def downUrlPicFromList(rfile,wfile, dstdir):
	#process child thread exception
	listecp = []

	try:
		file_object = open(rfile, 'r')
		file_w = open(wfile, 'w')

		while 1:
			url_pic = file_object.readline();
			url_pic.strip().lstrip().rstrip(',')
			print "url_pic: %s" % url_pic
			if not url_pic:
				break

			split_code="/"
			#slist = url_pic[url_pic.find(split_code)+5:]
			#slist = url_pic[url_pic.find(split_code[, 1][, 5])]
			print( url_pic.split('/')[5].split('\\')[0])
			#print slist

			try:
				#print "-----------------------1----------"
				#filesize = getTileEx(listecp, url_pic,dstdir + str(curid) + "." + format  )
				filesize = getTileEx(listecp, url_pic,dstdir + url_pic.split('/')[5]  )
				#print "filesize: %s" % filesize
				if int(filesize) > 20000 :
					#print "file: %s.%s is not exist..." % (curid, format)
					file_w.writeline(url_pic)
					#print "--------------"
				else:
					print "%s was download..."  % url_pic
					#file_w.writeline(url_pic)
				#os.getcwd()
			except Exception, e:
				file_object.close();
				file_w.close()
				print "\ngetTileEx exception happen"	
				raise GetPicException( url_pic)
		file_object.close()
		file_w.close()
		
	except GetPicException, e1:
		file_object.close()
		file_w.close()
		print e1
		print e1.name
		print "dddddddd"
		# store name of undownload file  to file
	except Exception , e:
		file_object.close()
		file_w.close()
		print e
		sys.exit()

	


if __name__ == '__main__':
	
	listfile = os.getcwd() + "\\" + "qrcodelist.txt"
	wfile = os.getcwd() + "\\" + "qrcodelist_bak.txt"
	dstdir = os.getcwd() + "\\pic_range\\" 
	print "dstdir: %s" % dstdir

	downUrlPicFromList( listfile , wfile, dstdir )