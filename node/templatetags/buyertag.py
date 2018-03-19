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
def buyersumbonus(value):
	from node.models import discountcard
	data=discountcard.objects.filter(buyer__id=value).aggregate(s=Sum('bonus'))['s']
	return mark_safe(data)
buyersumbonus.is_safe = True


@register.simple_tag
def buyer__discountcard__all(id):
	from node.models import buyer
	return discountcard.objects.filter(buyer__id=id)
	
	
@register.simple_tag
def buyer__eventcall__all(id):
	from panel.models import eventcall
	return eventcall.objects.filter(buyer__id=id)
	
	
@register.simple_tag
def buyer__smsqsend__all(id):
	from sms.models import smsqsend
	return smsqsend.objects.filter(buyer__id=id)
	
	
@register.simple_tag
def buyer__check__all(id):
	from node.models import check
	return check.objects.filter(buyer__id=id).order_by('-time')#[:5]