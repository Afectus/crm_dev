# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from django.db.models import Sum, Q, F, Count

from django.utils.safestring import mark_safe
from django.utils.numberformat import format

from django.contrib.auth.models import User, Group, UserManager

import datetime
import time

from django.core import serializers
import json

import re

from django import template

register = template.Library()


from node.models import *


#object to json
@register.filter
def objtojson(obj):
	#s = serializers.serialize('json', obj)
	data = {}
	data['id1c']=obj.id1c
	data['phone']=obj.phone
	data['f']=obj.f
	data['i']=obj.i
	data['o']=obj.o
	data['bday']=time.mktime(obj.bday.timetuple())
	data['sex']=obj.sex
	data['adv']=obj.adv
	#дисконтная карта
	if obj.discountcard_set.all():
		data['dcardid1c']=obj.discountcard_set.all().first().id1c
		data['dcardname']=obj.discountcard_set.all().first().name
		data['dcardbonus']=obj.discountcard_set.all().first().bonus
	else:
		data['dcardid1c']='def0'
		data['dcardname']='def0'
		data['dcardbonus']=0
	return json.dumps(data)
objtojson.is_safe = True

#object to json
@register.filter
def objtojson1(obj):
	#s = serializers.serialize('json', obj)
	data = {}
	data['pid1c']=obj.buyer.id1c
	data['pphone']=obj.buyer.phone
	data['id1c']=obj.id1c
	#data['f']=obj.f
	data['i']=obj.i
	data['o']=obj.o
	data['bday']=time.mktime(obj.bday.timetuple())
	data['type']=obj.type
	return json.dumps(data)
objtojson1.is_safe = True




#object to json
@register.filter
def getsumbonusallcards(obj):
	return obj.bonus
getsumbonusallcards.is_safe = True
