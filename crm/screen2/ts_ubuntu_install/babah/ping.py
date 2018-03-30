#!/usr/bin/python3


#cron
#*/5 * * * * /usr/bin/python3 /home/disc/ping.py > /dev/null
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

url = 'http://crm.babah24.ru/dev/ping/%s?crc=%s' % (mac, crc)
print(url)
r = requests.get(url)
print(r.json())


if r.json()['reboot'] == True:
    print("REBOOT")
    os.system('/bin/rm -R /home/babah/.cache/mozilla')
    os.system('/sbin/shutdown -r now')
