# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response



from django.db.models import Sum, Q, F, Count, TextField
from django.db.models.functions import Cast

from django.utils.safestring import mark_safe
from django.utils.numberformat import format

from django.contrib.auth.models import User, Group, UserManager

import re, datetime

from django import template

register = template.Library()


from node.models import *

@register.simple_tag
def report2_smssale(obj, idays):
	#obj = obj.buyer
	obj = obj.buyer.check_set.filter(time__gte=obj.cdate, time__lte=obj.cdate+datetime.timedelta(idays))
	# obj = obj.annotate(cg=Cast(F('checkitem__goods__name'),TextField())).annotate(cs=Sum('checkitem__col'))
	# from node.models import checkitem
	# try:
	# 	obj.data=checkitem.objects.get(fcheck=obj)
	# 	print obj.data.goods
	# except:
	# 	data=None
	
	return obj

# @register.simple_tag
# def report22_smssale_after(obj, date1):
# 	obj = obj.buyer.check_set.filter(time__gte=date1[0], time__lte=(date1[1]+datetime.timedelta(days=date1[2])))
# 	return obj
