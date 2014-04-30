#coding: utf-8
#!/usr/bin/env python
#filename: createIni.py 

from downmap import * 


if __name__ == '__main__':	
	createHrpcfg( "picturelist.xml", open("qysl.xml").read())