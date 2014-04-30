#encoding: utf-8
#/usr/bin/env python
# filename : checkfix.py

import os,sys,string
from PIL import Image

#修复问题文件，使用空文件替代
def checkfix( mappath, filetype):
		
	emptyimage = Image.open(".\empty.%s" % filetype.lower())
	filetype = filetype.upper()
	if(emptyimage.format != filetype):
		print "empty isn't exist or wrong"
		return

	#被修复的文件数
	count = 0
	

	#逐一检查目录下的所有文件
	filetype = filetype.lower()
	for root, dirs, files in os.walk(mappath): 
		for name in files: 
			curimagefile = 	os.path.join(root, name)
			#跳过其它类型的文件
			if( curimagefile.split('.')[-1]	!= filetype):				
				continue	
			try:		
				curimage = Image.open(curimagefile)
				
				if (curimage.format != filetype.upper()):
			  		emptyimage.save(curimagefile)  
			  		print "%s was fixed" % curimagefile
			  		count = count + 1			  		
			except:
				print "load or fix error"
				emptyimage.save(curimagefile)
		print "directory %s was checked" % root
	print "========There are %d file was fixed!===========" % count

if __name__ == '__main__':
	
	checkfix('E:\\try\qygzshiliang','png')