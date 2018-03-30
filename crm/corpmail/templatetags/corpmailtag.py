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


from corpmail.models import *

@register.simple_tag
def crm_recursion(obj):
	res = corpmail.objects.filter(corpmail=obj.corpmail).filter(Q(user=obj.user) | Q(addressee=obj.user)).order_by('id')
	return res

@register.simple_tag(takes_context=True)
def unread_letters(context):
	request = context["request"]
	# print request
	data=corpmail.objects.filter(addressee__user=request.user)
	return data.filter(status='created').count()

