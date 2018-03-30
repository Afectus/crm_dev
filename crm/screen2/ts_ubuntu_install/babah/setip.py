#!/usr/bin/python3


#cron
#*/59 * * * * /usr/bin/python3 /home/disc/setip.py > /dev/null
#

import requests
import hashlib
from uuid import getnode
import os

def makeapitoken(salt):
    apitoken='XXXXXX'
    crc = hashlib.md5()
    texts="%s:%s" % (salt, apitoken)
    crc.update(texts.encode('ascii'))
    crc=crc.hexdigest()
    return crc.upper()

mac=str(hex(getnode()))
#mac = '0xb827ebf04609'

crc = makeapitoken(mac)

try:
    import netifaces as ni
    ni.ifaddresses('enp3s0')
    ip = ni.ifaddresses('enp3s0')[2][0]['addr']
except:
    ip="cant_detected"


url = 'http://crm.babah24.ru/dev/setip/%s?ip=%s&crc=%s' % (mac, ip, crc)
print(url)
r = requests.get(url)
print(r.json())


