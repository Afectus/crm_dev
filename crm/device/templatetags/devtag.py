# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from node.models import *

from django.db.models import Sum
from django.db.models import Q

from django.utils.safestring import mark_safe
from django.utils.numberformat import format

from django.contrib.auth.models import User, Group, UserManager

import re

from django import template

register = template.Library()



'''
@register.filter
def ipsplitmask(value):
	return mark_safe(value)
ipsplitmask.is_safe = True
'''

@register.simple_tag
def devicelist(id):
	from device.models import device
	return device.objects.filter(Q(status=True), Q(promovideo=True) | Q(touchscreen=True) | Q(radiostream=True), Q(shopset__id=id)).order_by('name')
	
	
@register.simple_tag
def devicelistpromovideo(id):
	from device.models import device
	return device.objects.filter(Q(status=True), Q(promovideo=True), Q(shopset__id=id)).order_by('name')
