#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket, fcntl, struct, array, datetime

def getIfIP(ifStr):
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(sck.fileno(),0x8915,struct.pack('256s', ifStr[:15]))[20:24])

def getAllIf():
    max_possible = 128  # arbitrary. raise if needed.
    bytes = max_possible * 32
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    names = array.array('B', '\0' * bytes)
    outbytes = struct.unpack('iL', fcntl.ioctl(
        s.fileno(),
        0x8912,  # SIOCGIFCONF
        struct.pack('iL', bytes, names.buffer_info()[0])
    ))[0]
    namestr = names.tostring()
    return [namestr[i:i+32].split('\0', 1)[0] for i in range(0, outbytes, 32)]

def getIfIPToSay():
    ifs = getAllIf()
    if len(ifs)<2:
        return "Ни одного адреса для доступа не назначено"
    ip = getIfIP(ifs[-1]).replace("."," ")
    return "Адрес для доступа %s" % ip

def declension_ru(n, s1, s2, s5):
    ns = n % 10
    n2 = (n % 100)

    if n2 >= 10 and n2 <= 19:
        return s5

    if ns == 1:
        return s1

    if ns >=2 and ns <=4:
        return s2
    
    return s5    
    
def getTimeToSay():
    now = datetime.datetime.now()
    hour = declension_ru(now.hour, "час", "часа", "часов")
    minute = declension_ru(now.minute, "минута", "минуты", "минут")
    return "Текущее время %s %s %s %s" % (now.hour, hour, now.minute, minute)

def getMonthStr(month):
    return ('января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря')[month-1]

def getDateToSay():
    now = datetime.datetime.now()
    month = getMonthStr(now.month)
    return "Текущая дата %s %s %s года" % (now.day, month, now.year)

if __name__ == "__main__":
    print " --------------------------------- "
    print "| Module core tools. Version 1.0 |"
    print " --------------------------------- "

