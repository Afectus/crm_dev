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


def panelmenulist(context):
	from panel.models import panelmenu
	request = context['request']
	res = []
	data = panelmenu.objects.filter(parent__isnull=True).order_by('-sort')
	for i in data:
		tmp = {}
		tmp2=[]
		tmp['name']=i.name
		tmp['url']=i.url
		tmp['icon']=i.icon
		tmp['sub']=False
		tmp['select']=False
		#
		if request.path.rstrip("/") == i.url.rstrip("/"):
			tmp['select']=True
		pattern = re.compile("^(?P<path>.*)/?(?P<page>\d)/?$")
		regexdata = pattern.match(request.path)
		try:
			regexdata.group('path')
		except:
			pass
		else:
			#regexdata.group('path')
			if regexdata.group('path').rstrip("/") == i.url.rstrip("/"):
				tmp['select']=True	
		
		child = panelmenu.objects.filter(parent=i).order_by('-sort')
		for c in child:
			ctmp={}
			ctmp['name']=c.name
			ctmp['url']=c.url
			ctmp['icon']=c.icon
			ctmp['select']=False
			#
			#print request.path.rstrip("/"), '==', c.url.rstrip("/")
			if request.path.rstrip("/") == c.url.rstrip("/"):
				ctmp['select']=True
			pattern = re.compile("^(?P<path>.*)/?(?P<page>\d)/?$")
			regexdata = pattern.match(request.path)
			try:
				regexdata.group('path')
			except:
				pass
			else:
				#print regexdata.group('path'), '===', c.url.rstrip("/")
				#regexdata.group('path')
				if regexdata.group('path').rstrip("/") == c.url.rstrip("/"):
					ctmp['select']=True	
			#	
			tmp2.append(ctmp)

		if child.exists():
			tmp['sub']=True
			tmp['child']=tmp2
		res.append(tmp)

	return {'data': res, 'request': request,}
	#return {'data': res,}
register.inclusion_tag('_panelmenulist.html', takes_context=True)(panelmenulist)





#пути для моделей
@register.filter
def modelname(obj):
	return obj.model._meta.verbose_name
modelname.is_safe = True

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
	s = '<i class="fa fa-star text-primary" aria-hidden="true" style="color: gold;"></i> '
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


#обрезает срез пагинатора
def mypaginatorslice1(value, arg):
	srez=10
	l=len(value)
	if l <= srez:
		return range(1, l+1)
		
	if arg <= srez-1:
		return range(1, srez+1)

	tmp = srez
	while arg <= l-srez:
		if arg <= tmp-1:
			return range(arg, tmp)
		tmp=tmp+srez

	# if arg <= 10-1:
		# return range(1, 10)
	# if arg <= 20-1:
		# return range(10, 20)
	# if arg <= 30-1:
		# return range(20, 30)
	# if arg <= 40-1:
		# return range(30, 40)
	
	if arg >= l-srez:
		return range(l-srez, l+1)
		
	return range(500, 1000)
register.filter('mypaginatorslice1', mypaginatorslice1)



@register.simple_tag
def propget(id, code):
	#from node.models import propertiesvalue
	#return propertiesvalue.objects.filter(properties__status=True, goods__id=id)
	from node.models import properties, propertiesvalue
	try:
		data=propertiesvalue.objects.get(goods__id=id, properties__code=code)
	except:
		data=False
	return data



@register.simple_tag
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

	
@register.simple_tag
def proplist2(id):
	from node.models import propertiesvalue
	return propertiesvalue.objects.filter(goods__id=id, properties__code__in=['HIT', 'NEW','RECOMMEND', ], value='YES')
	
	
@register.simple_tag
def naborlist(id):
	from node.models import goods
	return goods.objects.filter(naborparent_id=id)[:3]
	
	
	

	
	
	
@register.simple_tag
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







@register.filter
def percentofdigit(total, args):
	#1040 составляет 100%
	#800 составляет x%
	#x=800*100:1040=77% (77% в цифре 800 от 1040)
	#100%-77%=23% (на 23% число 800 меньше 1040)
	#data=float(args)*100/float(value)
	data = 0
	if total != 0: #ZeroDivisionError: integer division or modulo by zero
		data=(float(args)*100)/float(total)
	return mark_safe(data)
percentofdigit.is_safe = True
