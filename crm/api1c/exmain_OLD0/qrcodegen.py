#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, django

projecthome = '/var/www/crm/'
if projecthome not in sys.path:
    sys.path.append(projecthome)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj.settings")
django.setup()



import time
import requests
import datetime
from django.utils import timezone
import qrcode
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from node.models import *
from dj.views import *



salt = id_generator() #создаем сессию соль
token = makeapitoken(salt) #подписываем соль
#print salt, token


g=goods.objects.all()
for i in g:
	i.qrcode.delete()

g=goods.objects.filter(idbitrix__isnull=False, status=True).exclude(idbitrix__exact='') #товары только с idbitrix, исключаем пустые


for i in g:
	print "MAKE QRCODE ID %s" % i.idbitrix
	qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=100, border=1,)
	#url = 'http://babah24.ru/katalog/detail.php?ELEMENT_ID=%s' % i.idbitrix
	url = 'http://babah24.ru/qr/%s' % i.idbitrix
	qr.add_data(url)
	qr.make(fit=True)

	#img = qr.make_image(fill_color="#FF6600", back_color="white")
	img = qr.make_image(fill_color="white", back_color="black")
	#img = qr.make_image(fill_color="black", back_color="white")

	buffer = StringIO.StringIO()
	img.save(buffer)
	filename = '%s.png' % id_generator()
	filebuffer = InMemoryUploadedFile(buffer, None, filename, 'image/png', buffer.len, None)
	i.qrcode.save(filename, filebuffer)
