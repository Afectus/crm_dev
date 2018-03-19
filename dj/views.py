# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponsePermanentRedirect

from django.core.exceptions import PermissionDenied

from django.views.generic import DetailView, ListView, DeleteView
from django.views.generic.edit import FormView, UpdateView
from django.views.generic.base import TemplateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

import datetime
import string
import random
import hashlib
import re
import barcode

from django.conf import settings





#@group_required('admins','editors')
#def myview(request, id):
#...
'''
def group_required(*group_names):
	from django.contrib.auth.decorators import user_passes_test
	"""Requires user membership in at least one of the groups passed in."""
	def in_groups(u):
		if u.is_authenticated():
			if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
				return True
		return False
	return user_passes_test(in_groups)
'''

	
	
def makeapitoken(salt):
	apitoken=settings.MAKEAPITOKEN_TOKEN
	crc = hashlib.md5()
	crc.update(('%s:%s' % (salt, apitoken)).encode('utf-8'))
	crc=crc.hexdigest()
	return crc.upper()


def password_generator():
	#symbols = ['q','w','e','r','t','y','u','i','o','p','s','a','d','f','g','h','j','k','l','z','x','c','v','b','n','m']
	#symbols = ['1','2','3','4','5','6','7','8','9',\
	#'w','e','t','y','o','p','s','a','k','z','x','c','v','b','m', \
	#'1','2','3','4','5','6','7','8','9']
	symbols = ['q','w','e','r','t','y','u','i','o','p','s','a','d','f','g','h','j','k','z','x','c','v','b','n','m','1','2','3','4','5','6','7','8','9']
	symbols = ['1','2','3','4','5','6','7','8','9']
	i = 0
	password = ''
	while i < 8:
		tempsymbol = ''
		tempsymbol += random.choice(symbols)
		#temp = random.randint(0,1)
		#if temp == 1:
		#	password += tempsymbol.upper()
		#else:
		#	password += tempsymbol
		password += tempsymbol
		i += 1
	return password
	
def sms_generator():
	symbols = ['1','2','3','4','5','6','7','8','9']
	i = 0
	sms = ''
	while i < 6:
		tempsymbol = ''
		tempsymbol += random.choice(symbols)
		sms += tempsymbol
		i += 1
	return sms
	

def md5_generator(value):
	m = hashlib.md5()
	m.update(value.encode('utf-8'))
	return m.hexdigest()


#генератор случайностей
def id_generator(size=24, chars=string.ascii_letters + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

#функция записи файлов из моделей filefield imagefield, что бы не было гемора с кириллицей
def make_upload_path(instance, filename):
	category = instance.__class__.__name__ #имя модели, каталог категория
	filename = id_generator()
	return u"uploads/%s/%s" % (category, '%s.png' % filename)
	
def make_upload_file(instance, filename):
    category = instance.__class__.__name__ #имя модели, каталог категория
    fileext = re.compile(r'^.*\.(?P<ext>\w+)$').match(filename).group('ext')
    filename = id_generator()
    return u"uploads/%s/%s" % (category, '%s.%s' % (filename, fileext))	

	
#генератор случайностей
def backlink_generator(size=6, chars=string.ascii_letters + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))
	
	
#генератор штрихкода EAN13
def genbarcode(mode, salt=0):
	#pip3 install python-levenshtein pyBarcode
	#import random, barcode
	#mode
	#1 - , 2 - goods, 3 - materialvalue, 4 - goods, 5 - , 6 - goods , 7 - , 8 - goods, 9 -
	#salt - only digit, example id
	#example
	#312365498745
	#|-first digit 3 mode materialvalue
	##|||-id materialvalue
	#####||||||||-random digit
	totallen=11
	leftlen=len(str(salt))
	a=totallen-leftlen
	randleft='1'+('0'*(a-1))
	randright='9'*a
	randdigit=random.randint(int(randleft), int(randright))
	res='%s%s%s' % (mode, salt, randdigit)
	ean = barcode.get('ean13', res)
	#print('%s - %s -> %s' % (salt, res, ean.get_fullcode()))
	return ean
	
	

	
	