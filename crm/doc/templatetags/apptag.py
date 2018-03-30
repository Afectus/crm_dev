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


@register.filter
def mybool(value):
	if value:
		msg = u'Да'
	else:
		msg = u'Нет'
	return msg
mybool.is_safe = True

@register.filter(is_safe=True)
def myboolicon(value):
	if value:
		msg = u'<span class="text-green"><i class="fa fa-check-square-o" aria-hidden="true"></i></span>'
	else:
		msg = u'<span class="text-danger"><i class="fa fa-times" aria-hidden="true"></i></span>'
	return mark_safe(msg)

#вместо flotaformat, для 0.25 разделитель всегда точка
@register.filter
def floatdot(value, decimal_pos=0):
    #return format(value, ".%sf" % decimal_pos)
	return format(value, ".", decimal_pos)
floatdot.is_safe = True


#может работать через встроенные фильтры {{ i.src|slice:"7:11" }}
#@register.filter(is_safe=True)
def hidephone(value):
	left=len(value)-4
	right=len(value)
	filler='X'*left
	res='%s%s' % (filler, value[left:right])
	return res

register.filter('hidephone', hidephone)



#обрезает срез пагинатора
def mypaginatorslice(value, arg):
	lenp=len(value)+1
	srez=5 #сколько срезать
	start=arg-srez
	if start < 0: #если начало среза меньше 0 присвоить 0
		start=1
	end=arg+srez
	if end >= lenp:
		end=lenp
	value=range(start, end)
	return value

register.filter('mypaginatorslice', mypaginatorslice)


	
@register.simple_tag
def proplist(id):
	return propertiesvalue.objects.filter(goods__id=id, properties__code__in=['HIT', 'NEW','RECOMMEND', ], value='YES')
	
	
	
