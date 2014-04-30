#coding: utf-8
#! /usr/bin/env python
#filename: writefile.py

#from xml.etree import ElementTree
from xml.etree.ElementTree import Element, tostring, fromstring
from xml.etree import ElementTree
import uuid
import os,sys,string,time
from getTile import *
import thread,threading


def mkdir(path):
	# invoke module
	#import os

	#去除首尾空格
	path = path.strip()
	#去除尾部 \符号
	path = path.rstrip("\\")

	#判断路径是否存在
	#存在 True
	#不存在 False
	isExist = os.path.exists(path)

	#判断结果
	if not isExist:		
		#创建目录操作函数
		os.makedirs(path)
		return True
	else:
		#如果目录存在则不创建，并提示目录已存在		
		return False

#生成HRP数据配置文件
def createHrpcfg(hrpcfgfile, configfile):
	
	#图层数据范围
	GEOSTARTX="111.80"
	GEOSTARTY="25.2"
	GEOENDX="114.00"
	GEOENDY="23.40"

	root = ElementTree.fromstring( configfile )

	node_ip = root.find('IP')
	node_port = root.find('Port')
	node_map = root.find('Map')
	node_style = root.find('Style')
	node_ucrs = root.find('uCrs')
	node_ext = root.find('EXT')

	# 获取element的方法
    # 1 通过getiterator 
	lst_node = root.getiterator("TileMatrix")

	#curdir = "%s/%s" % (path,node_map.text)
	#print curdir
	#print "%s/%s" % (mappath,node_identifier.text[10:]) 
	#mkdir(curdir)
    
	parent_uuid = uuid.uuid1()

	#创建xml文件
	#1 生成根节点
	myRoot = Element('picturelist')
	tree = ElementTree.ElementTree(myRoot)
	sumpicName = ""
	sumuuid = ""
	
	for node in lst_node:
		node_identifier = node.find("Identifier")
		node_rowstart = node.find("RowStart")
		node_rowend = node.find("RowEnd")
		node_colstart = node.find("ColStart")
		node_colend = node.find("ColEnd")
		node_scale = node.find("ScaleDenominator")
		node_resolution = node.find("Resolution")
		
		tileWidth = 256
		tileHeight = 256
		
		picuuid = uuid.uuid1()

		
		#2 生成子节点
		myChild = Element('picture',{'name': "%s_%s" % (node_map.text, node_identifier.text[10:]),
			'parentname':"%s" % node_map.text,
			'path':"/hrp/data/%s/%s_%s/" % (node_map.text,node_map.text,node_identifier.text[10:]),
			'description':"",
			'width':"%d" % ((int(node_colend.text) - int(node_colstart.text) +1)*tileWidth),
			'height':"%d" % ((int(node_rowend.text) - int(node_rowstart.text) +1)*tileHeight),
			'blockwidth':"%d" % tileWidth,
			'blockheight':"%d" % tileHeight,
			'scale':"%s" % node_scale.text,
			'geocoor_start_x':GEOSTARTX,#"%f" % (-180+(int(node_colstart.text)-1)*256*float(node_resolution.text)),
			'geocoor_start_y':GEOSTARTY,#"%f" % (90-(int(node_rowstart.text)-1)*256*float(node_resolution.text)),
			#'geocoor_end_x':"%f" % (float(GEOSTARTX)+(float(node_colend.text)-float(node_colstart.text)+1)*256*float(node_resolution.text)),
			#'geocoor_end_y':"%f" % (float(GEOSTARTY)+(float(node_rowend.text)-float(node_rowstart.text)+1)*256*float(node_resolution.text)),
			'geocoor_end_x':GEOENDX,
			'geocoor_end_y':GEOENDY,
			'sumpic_name':sumpicName,
			'transcolor':"0",
			'blocknuminterval':"0",
			'blknumrange_start_m':"0",#node_rowstart.text,
			'blknumrange_start_n':"0",#node_colstart.text,
			'blknumrange_end_m':str(int(node_rowend.text)-int(node_rowstart.text)),
			'blknumrange_end_n':str(int(node_colend.text)-int(node_colstart.text)),
			'pic_uuid':"%s" % picuuid,
			'sum_uuid':"%s" % sumuuid,
			'parent_uuid': "%s" % parent_uuid})

		sumpicName = "%s_%s" % (node_map.text, node_identifier.text[10:])
		sumuuid = picuuid

		myRoot.append(myChild)		

	prettyXml(myRoot,'\t', '\n')
	tree.write(hrpcfgfile)	
	print "HRP data config file was created success!"

# 根据配置文件下载数据，若数据下载过程中出现断开，再次下载时从上次下载结束的位置进行数据下载
def downMapEx(mappath, configfile):	

	# multithread
	threads = []

	#process child thread exception
	listecp = []

	# progressbar
	total = 0
	curfinish = 0
	uprate = 30 # 进度条更新频率，每下载10个图片，更新一次进度条

    # 加载XML文件（2种方法,一是加载指定字符串，二是加载指定文件）    
    # root = ElementTree.parse(r"D:/test.xml")
	root = ElementTree.fromstring( configfile )

	node_ip = root.find('IP')
	node_port = root.find('Port')
	node_map = root.find('Map')
	node_style = root.find('Style')
	node_ucrs = root.find('uCrs')
	node_ext = root.find('EXT')


	# 从下载配置文件中读取已经下载的配置
	if(os.path.isfile('getTileErr.ini')):		
		pidentifier = preIdentifier = readIni("getTileErr.ini",node_map.text,"identifier")	
		pi = preRow = readIni("getTileErr.ini",node_map.text,"row")
		pj = preCol = readIni("getTileErr.ini",node_map.text,"col")
		pcurfinish = curfinish = readIni("getTileErr.ini", node_map.text,"num" )
		print "downloaded: ident:%s, row:%s, col:%s" % (preIdentifier,preRow, preCol)
		# 用于路过多于的配置文件判断
		isSkip = False
	else:
		pidentifier = preIdentifier = "0"
		pi = preRow = 0
		pj = preCol = 0
		pcurfinish = curfinish = 0
		isSkip = True

	
	
    # 获取element的方法
    # 1 通过getiterator 
	lst_node = root.getiterator("TileMatrix")  

	#统计
	for node in lst_node:		
		total = total + (int(node.find("RowEnd").text) - int(node.find("RowStart").text) + 1)*(int(node.find("ColEnd").text) - int(node.find("ColStart").text)+ 1)
	
	print "total:= %d tiles will be download" % total

	

	try:
		#分层下载数据
		for node in lst_node:
			node_identifier = node.find("Identifier")
			if ((cmp(node_identifier.text[10:],preIdentifier) != 0) and (isSkip == False)):
				print "identifier %s was skip" % node_identifier.text
				continue
			else:
				#print "isSkip was set true"
				isSkip = True
			node_rowstart = node.find("RowStart")
			node_rowend = node.find("RowEnd")
			node_colstart = node.find("ColStart")
			node_colend = node.find("ColEnd")

			# 为当前比例尺创建文件夹存放数据
			curdir = "%s/%s/%s_%s" % (mappath,node_map.text,node_map.text,node_identifier.text[10:])		
			mkdir(curdir)

			startTime = time.clock()

			for i in range(int(node_rowstart.text), int(node_rowend.text) + 1):
				if i < int(preRow):
					#print "row:%s was skip" % i										
					continue
				else:
					#print "prerow was set 0"
					preRow = 0
				# create a row directory
				rowcur = i-int(node_rowstart.text)
				#print "rowcur: %s" % rowcur
				rowcurdir = "%s/%s/%s_%s/%s" % (mappath,node_map.text,node_map.text,node_identifier.text[10:],rowcur)
				#print "rowcurdir: %s" %  rowcurdir	
				mkdir(rowcurdir)
				for j in range(int(node_colstart.text), int(node_colend.text) + 1):
					if j < int(preCol):
						#print "col:%s was skip" % j
						continue
					else:
						#print "precol was set 0"
						preCol = 0
					url = "http://%s:%s/wmts/%s/%s/%s/%s/%s/%s.%s" % (node_ip.text,
							node_port.text, node_map.text,node_style.text,node_ucrs.text, node_identifier.text[10:], i, j, node_ext.text)
					
					#tag = "%s_%d_%d_%d" % (node_identifier.text[10:], i, j, curfinish)
					try:
						#print "gettile: row:%s, col: %s" % (i, j)
						#thrd = threading.Thread(target=getTile, args=(url,"%s/%s_%s.%s" % (curdir, i-int(node_rowstart.text), j-int(node_colstart.text), node_ext.text), ))
						thrd = threading.Thread(target=getTileEx, args=(listecp,url,"%s/%s.%s" % (rowcurdir, j-int(node_colstart.text), node_ext.text), ))
						thrd.start()
						threads.append(thrd)
						#thread.start_new_thread( getTile, (url,"%s/%s_%s.%s" % (curdir, i-int(node_rowstart.text), j-int(node_colstart.text), node_ext.text), ) )
						#getTile(url, "%s/%s_%s.%s" % (curdir, i-int(node_rowstart.text), j-int(node_colstart.text), node_ext.text))
						
						
					except Exception, e:
						print e
						raise GetTileExcption(node_identifier.text[10:], i, j, curfinish )
						
					curfinish = int(curfinish) + 1

					if( curfinish%uprate == 0 ):		#每下载10个切片更新一下进度
						# 等待一批切片的完成
						for t in threads:
							t.join()
						threads = []

						if (len(listecp) == 0):
							pass
						else:
							print "\nexception happen"	
							raise GetTileExcption( pidentifier, pi, pj, pcurfinish )

						
						pi = i
						pj = j 
						pidentifier = node_identifier.text[10:]
						pcurfinish = curfinish

						endTime = time.clock()
						view_bar(curfinish, total, (endTime - startTime)*(total-curfinish)/uprate)												

						startTime = time.clock()  #用于统计时间

			print "\rTileMatrix: %s is OK !" % node_identifier.text[10:]
		print "\rAll download finished!"

		# clear a
		for t in threads:
			#print "t.join(2)"
			t.join()

		if (os.path.isfile('getTileErr.ini')):
			os.remove("getTileErr.ini")
	except GetTileExcption, ex:
		if ((ex.row == 0) and (ex.col == 0)):
			print "download failed "
			print "please check network!!!"
			print "sleep 10 seconds"
			time.sleep(10)	
			print "try download again!"	
			downMapEx(mappath, configfile)

		if (os.path.isfile('getTileErr.ini')):
			os.remove("getTileErr.ini")
		ini = opIni("getTileErr.ini")
		ini.writeIni(node_map.text,"Identifier",ex.identifier);
		ini.writeIni(node_map.text,"row",ex.row )
		ini.writeIni(node_map.text,"col",ex.col )
		ini.writeIni(node_map.text,"num",ex.num )
		ini.closeIni()
		print "download tile %s:%s_%s.png failed" % (ex.identifier,ex.row, ex.col )
		print "please check network!!!"
		print "sleep 10 seconds"
		time.sleep(10)	
		print "try download again!"	
		downMapEx(mappath, configfile)

		#sys.exit()
	except Exception , e:
		print e
		sys.exit()


#element 为传进来的Element类， 参数indent用于缩进, newline用于换行
#格式化xml
def prettyXml(element, indent, newline, level=0): 
	if len(element):
		if element.text == None or element.text.isspace():
			element.text = newline + indent * (level + 1)
		else:
			element.text = newline + indent *(level+1) + element.text.strip() + newline + indent * (level +1)
	temp = list(element)
	for subelement in temp:
		if temp.index(subelement) < (len(temp) - 1):
			subelement.tail = newline + indent * (level + 1)
		else:
			subelement.tail = newline + indent * level
		prettyXml(subelement, indent, newline, level + 1)

# 显示进度条
def view_bar(num=1, sum=100,timeleft = 0, bar_word="="):  
   print '\r%d/%d :' % (num,sum),   
   for i in range(0, num, int(sum/20)):   
       os.write(1, bar_word)   
   os.write(1,"Estimated Download Time: %dhours %d minitues %d seconds" % (timeleft/3600, (timeleft%3600)/60, timeleft%60))
   sys.stdout.flush() 
   #print "Estimated Download Time: %dhours %d minitues %d seconds" % (timeleft/3600, (timeleft%3600)/60, timeleft%60)
 	
# 写配置文件
import ConfigParser
class opIni(object):
	"""docstring for opIni"""
	def __init__(self, filename):
		super(opIni, self).__init__()
		self.filename = filename
		self.config = ConfigParser.ConfigParser()
		self.config.optionxform = str

	def writeIni(self, section, option, value ):
				
		# set a number of parameters
		if( not self.config.has_section(section)):
			self.config.add_section( section )

		if( not self.config.has_option(section, option)):
			self.config.set(section,option,value)
		#config.write(open(file, "w+"))

	def closeIni(self):
		self.config.write(open(self.filename, "w+"))

# 写配置文件
def readIni(file, section, option):	
	config = ConfigParser.ConfigParser()
	config.readfp(open(file))
	return config.get(section,option)


if __name__ == '__main__':	
	if (cmp(os.name,"nt") == 0):
		datapath = "d:/data"
		print "cur os is windows"		
	elif(cmp(os.name,"posix") == 0):
		datapath = "/hrp/data"
		print "cur os is linux"
	print "datapath:%s" % datapath
	#createHrpcfg( datapath, open("qysl.xml").read())
	downMapEx( datapath, open("qysl.xml").read())

