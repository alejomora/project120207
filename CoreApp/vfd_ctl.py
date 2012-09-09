#!/usr/bin/python
# -*- coding: utf-8 -*-

import feedparser
import time
import datetime
from serial import Serial, struct

tbl={}

def initTbl():
	utfChrs = u'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
	utfChrs2= u'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
	asciiOrd=0xA0
	for utfChr in utfChrs:
		tbl[utfChr]=asciiOrd
		asciiOrd=asciiOrd+1
	asciiOrd=0xA0
        for utfChr in utfChrs2:
                tbl[utfChr]=asciiOrd
                asciiOrd=asciiOrd+1

	#print tbl

def conv(inStr):
	outStr='';
	for chrInStr in inStr:
		if chrInStr in tbl.keys():
			outStr = outStr + chr(tbl[chrInStr])
		else:
			outStr = outStr + chrInStr.encode('ascii')
	return outStr

def disp_goto(x, y):
	pos = x + y * 20;
	return struct.pack('BB',0x1b,pos);

def get_rss(strURL):
	objRSS = feedparser.parse(strURL)
	strRSS=u''
	for entryRSS in objRSS.entries:
		strRSS = strRSS + "|" + entryRSS.title
	return strRSS

def init_run_rss(strRSS):
	structRSS = {}
	structRSS['strRSS'] = strRSS + ' '
	structRSS['pos'] = 0
	return structRSS	

def run_rss(structRSS):
	outStr = structRSS['strRSS'][structRSS['pos']:20+structRSS['pos']]
	structRSS['pos'] = structRSS['pos'] + 4
	if structRSS['pos'] >= len(structRSS['strRSS']):
		structRSS['pos'] = 0
	return outStr
	
	
initTbl()

ser = Serial('/dev/ttyUSB0', 9600)

#ser.write(struct.pack('B',0x19))
#ser.write(struct.pack('B',0x3E))

ser.write(struct.pack('B',0x14))
ser.write(struct.pack('B',0x1E))
ser.write(struct.pack('B',0x0E))
ser.write(disp_goto(0, 0))
ser.write(conv(u"Получаем новости..."))
uStrRSS = get_rss("http://news.yandex.ru/index.rss")
print uStrRSS 
strRSS = conv(uStrRSS)
structRSS = init_run_rss(strRSS)
ser.write(struct.pack('B',0x15))
ser.write(conv(u"Время:"))
syncNow = True
while True:
	now = datetime.datetime.now()
	ser.write(disp_goto(6, 0))
	ser.write("%02d:%02d:%02d" % (now.hour, now.minute, now.second))
	time.sleep(1)
	ser.write(disp_goto(0, 1))
	ser.write(run_rss(structRSS))
	
	if (now.minute == 31 or now.minute == 1) and not syncNow:
		syncNow = True
	
	if (now.minute == 30 or now.minute == 0) and syncNow:
		syncNow = False
		ser.write(struct.pack('B',0x15))
		ser.write(conv(u"Получаем новости..."))
		uStrRSS = get_rss("http://news.yandex.ru/index.rss")
		strRSS = conv(uStrRSS)
		structRSS = init_run_rss(strRSS)
		ser.write(struct.pack('B',0x15))
		ser.write(conv(u"Время:"))

