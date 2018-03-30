#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, django

projecthome = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if projecthome not in sys.path:
    sys.path.append(projecthome)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj.settings")
django.setup()



import time
import requests
import datetime
from django.utils import timezone

from node.models import *
from panel.models import *
from node.views import *
from panel.views import *

from dj.views import *


media='media'

#############################PICT
pre='uploads/goods'
checkpath = "%s/%s" % (media, pre)

flist = [f for f in os.listdir(checkpath) if os.path.isfile(os.path.join(checkpath, f))]



for i in flist:
	fpath = '%s/%s' % (pre, i)
	try:
		r=goods.objects.get(pict=fpath)
	except:
		print "DELETE pict %s" % fpath
		os.unlink('%s/%s' % (media, fpath)) #удаляем временный файл
		#print os.path.exists(f.name) #проверяем доступен ли временный файл после удаления

#ls -1 goods | wc -l
flist = [f for f in os.listdir(checkpath) if os.path.isfile(os.path.join(checkpath, f))]
print len(flist)


#############################QRCODE
pre='uploads/qrcode'
checkpath = "%s/%s" % (media, pre)

flist = [f for f in os.listdir(checkpath) if os.path.isfile(os.path.join(checkpath, f))]

for i in flist:
	fpath = '%s/%s' % (pre, i)
	
	try:
		r=goods.objects.get(qrcode=fpath)
	except:
		print "DELETE qrcode %s" % fpath
		os.unlink('%s/%s' % (media, fpath)) #удаляем временный файл
		#print os.path.exists(f.name) #проверяем доступен ли временный файл после удаления


#ls -1 goods | wc -l
flist = [f for f in os.listdir(checkpath) if os.path.isfile(os.path.join(checkpath, f))]
print len(flist)


