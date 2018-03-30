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


#подсчет количества остатков
@register.filter
def getgoodsinstockvalue(obj):
	data = goodsinstock.objects.filter(goods=obj).aggregate(count=Sum('value'))
	return data['count']
getgoodsinstockvalue.is_safe = True



'''
@register.filter
def modellinkadd(obj):
	return mark_safe('<a href="/%s/add/" class="btn btn-success"><i class="fa fa-plus" aria-hidden="true"></i></a>' % (obj.model.__name__))
modellinkadd.is_safe = True

@register.filter
def modellinkedit(obj):
	return mark_safe('<a href="/%s/edit/%s/" class="btn btn-success"><i class="fa fa-pencil" aria-hidden="true"></i></a>' % (obj.__class__.__name__, obj.id))
modellinkedit.is_safe = True

@register.filter
def modellinkdel(obj):
	return mark_safe('<a href="/%s/del/" class="btn btn-success"><i class="fa fa-trash" aria-hidden="true"></i></a>' % (obj.__class__.__name__, obj.id))
modellinkdel.is_safe = True
#




#подсчет плана магазина
@register.filter
def total_nal(value):
	from node.models import check
	data=check.objects.filter(time__range=(value.sdate, value.edate), shop=value.shop)
	return float(data.aggregate(c=Sum('nal'))['c'] or 0)

@register.filter
def total_beznal(value):
	from node.models import check
	data=check.objects.filter(time__range=(value.sdate, value.edate), shop=value.shop)
	return float(data.aggregate(c=Sum('beznal'))['c'] or 0)

@register.filter
def total_all(value):
	from node.models import check, checkitem
	data=checkitem.objects.filter(fcheck__time__range=(value.sdate, value.edate), fcheck__shop=value.shop)
	return float(data.aggregate(c=Sum('sum'))['c'] or 0)
	
@register.filter
def total_check(value):
	from node.models import check, checkitem
	data=check.objects.filter(time__range=(value.sdate, value.edate), shop=value.shop)
	return data.count()
#######################

@register.filter
def buyerdetail(value):
	return mark_safe('<a href="/buyer/detail/%s">%s %s %s</a>' % (value.id, value.f, value.i, value.o))
buyerdetail.is_safe = True


@register.filter
def who(value):
	from panel.models import profileuser
	pu=profileuser.objects.get(user=value)
	return mark_safe('<a href="/personal/detail/%s">%s %s</a>' % (pu.id, value.first_name, value.last_name))
who.is_safe = True

@register.filter
def ratingstar(value):
	s = '<i class="fa fa-star text-primary" aria-hidden="true"></i> '
	so = '<i class="fa fa-star-o" aria-hidden="true"></i> '
	res = s*value
	res = res + (so*(5-value))
	return mark_safe(res)
ratingstar.is_safe = True

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


@register.assignment_tag
def proplist(id):
	#from node.models import propertiesvalue
	#return propertiesvalue.objects.filter(properties__status=True, goods__id=id)
	from node.models import properties
	res = []
	data=properties.objects.filter(status=True, propertiesvalue__goods__id=id).distinct()
	for i in data:
		tmp = {}
		tmp['name'] = i.name
		tmp['baseunit'] = i.baseunit
		tmp['multiple'] = i.multiple
		if i.multiple:
			m=[]
			for p in i.propertiesvalue_set.filter(properties__id=i.id, goods__id=id):
				m.append(p.value)
			tmp['value'] = m
		else:
			tmp['value'] = i.propertiesvalue_set.filter(properties__id=i.id, goods__id=id).first().value
		res.append(tmp)
	return res

	
@register.assignment_tag
def proplist2(id):
	from node.models import propertiesvalue
	return propertiesvalue.objects.filter(goods__id=id, properties__code__in=['HIT', 'NEW','RECOMMEND', ], value='YES')
	
	
@register.assignment_tag
def naborlist(id):
	from node.models import goods
	return goods.objects.filter(naborparent_id=id)[:3]
	
	
	
@register.assignment_tag
def lastcheck(id):
	from node.models import check
	return check.objects.filter(buyer__id=id).order_by('-time')[:5]
	
	
	
@register.assignment_tag
def getprofileuser(id):
	from panel.models import profileuser
	return profileuser.objects.get(user__id=id)
	
	
@register.filter
def shopgetcolor(value):
	from node.models import shop
	try:
		data=shop.objects.get(id=value).htmlcolor
	except:
		data=None
	return data
shopgetcolor.is_safe = True
'''