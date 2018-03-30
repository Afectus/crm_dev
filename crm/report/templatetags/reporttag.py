# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response


from django.db.models import Sum, Q, F, Count

from django.utils.safestring import mark_safe
from django.utils.numberformat import format

from django.contrib.auth.models import User, Group, UserManager

import re

from django import template

register = template.Library()

from node.models import *

@register.filter
def reportchecksumnodiscount(obj):
	return checkitem.objects.filter(fcheck=obj).aggregate(c=Sum(F('price')*F('col')))['c']

@register.filter
def reportchecksumdiscount(obj):
	value = checkitem.objects.filter(fcheck=obj).aggregate(c=Sum('checkd__discount'))['c']
	return value
	
	
@register.filter
def reportchecksum(obj):
	return checkitem.objects.filter(fcheck=obj).aggregate(c=Sum('sum'))['c']
	
@register.filter
def reportgetshop(value):
	#from node.models import *
	try:
		data=shop.objects.get(id=value).name
	except:
		data=None
	return data
reportgetshop.is_safe = True



	
	
	