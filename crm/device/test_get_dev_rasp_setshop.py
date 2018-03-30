#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import requests

os.system("/var/www/crm/crmkill");




r = requests.get("http://crm.babah24.ru/dev/get/%s" % ('0xb827ebdeb575'))
print r.json()

data = r.json()

for i in data['data']:
    print i