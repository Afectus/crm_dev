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
from worktask.models import *

@register.filter
def reportchecksumnodiscount(obj):
	return checkitem.objects.filter(fcheck=obj).aggregate(c=Sum(F('price')*F('col')))['c']

@register.filter
def reportchecksumdiscount(obj):
	return checkitem.objects.filter(fcheck=obj).aggregate(c=Sum('checkd__discount'))['c']
	
@register.filter
def reportchecksum(obj):
	return checkitem.objects.filter(fcheck=obj).aggregate(c=Sum('sum'))['c']
	

@register.simple_tag(takes_context=True) 
def newtask(context, obj):
	request = context["request"]
	a=notificationtask.objects.filter(usertask=obj, usertask__executor__user=request.user, user=request.user)
	return a.exists()
	

#не прочитанные задания
@register.simple_tag(takes_context=True) 
def unreadtask(context):
	request = context["request"]
	nt=notificationtask.objects.filter(user=request.user)
	data=usertask.objects.filter(executor__user=request.user, status='open').exclude(notificationtask__in=nt)
	return data
		

		

	
	
	