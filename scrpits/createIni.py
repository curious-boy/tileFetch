#coding: utf-8
#!/usr/bin/env python
#filename: createIni.py 

from downmap import * 

def createIni(inifile,configfile):
	#图层数据范围
	GEOSTARTX="111.80"
	GEOSTARTY="23.40"
	GEOENDX="114.00"
	GEOENDY="25.2"

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

	
	#创建xml文件
	#1 生成根节点
	
	sumpicName = ""	
	
	if (os.path.isfile(inifile)):
		os.remove(inifile)
	ini = opIni( inifile )
	i = 0

	for node in lst_node:
		node_identifier = i
		node_rowstart = node.find("RowStart")
		node_rowend = node.find("RowEnd")
		node_colstart = node.find("ColStart")
		node_colend = node.find("ColEnd")
		node_scale = node.find("ScaleDenominator")
		node_resolution = node.find("Resolution")
		
		tileWidth = 256
		tileHeight = 256
		

		ini.writeIni(str(node_identifier),"mapLeftLon",GEOSTARTX);
		ini.writeIni(str(node_identifier),"mapRightLon",GEOENDX);
		ini.writeIni(str(node_identifier),"mapTopLat",GEOENDY);
		ini.writeIni(str(node_identifier),"mapBottomLat",GEOSTARTY);
		ini.writeIni(str(node_identifier),"width","%d" % ((int(node_colend.text) - int(node_colstart.text) +1)*tileWidth));
		ini.writeIni(str(node_identifier),"height","%d" % ((int(node_rowend.text) - int(node_rowstart.text) +1)*tileHeight));
		ini.writeIni(str(node_identifier),"Scale",node_scale.text);
		ini.writeIni(str(node_identifier),"tilewidth",tileWidth);
		ini.writeIni(str(node_identifier),"tileheight",tileHeight);
		ini.writeIni(str(node_identifier),"SumPic",sumpicName);

		sumpicName = "%s" %  node_identifier
		i = i+1

	ini.closeIni()	
	
	print "inifile was created success!"

if __name__ == '__main__':
	createIni("Tile.ini",open("qysl.xml").read())