#!/usr/bin/python3

import requests
import hashlib
from uuid import getnode


def makeapitoken(salt):
    apitoken='1111'
    crc = hashlib.md5()
    texts="%s:%s" % (salt, apitoken)
    crc.update(texts.encode('ascii'))
    crc=crc.hexdigest()
    return crc.upper()

mac=str(hex(getnode()))
print(mac)
#mac = '0xb827ebf04609'

crc = makeapitoken(mac)

print(crc)

url = 'http://crm.babah24.ru/dev/ping/%s?crc=%s' % (mac, crc)
print(url)
r = requests.get(url)
print(r.json())
