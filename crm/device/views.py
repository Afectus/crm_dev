# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponsePermanentRedirect

from django.core.exceptions import PermissionDenied

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django import forms
from django.contrib.auth.models import User, Group

import json
from django.core import serializers

from django.http import QueryDict

from django.views.generic import DetailView, ListView, DeleteView
from django.views.generic.edit import FormView, UpdateView
from django.views.generic.base import TemplateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator

import datetime, time

from django.db.models import Sum, Count, Q, IntegerField
from django.db.models.functions import Cast

from django.views.decorators.csrf import csrf_exempt

#from node.templatetags.nodetags import node_count

from node.models import *
from device.models import *

from dj.views import *

from sqlalchemy import cast, Numeric, Column, Integer, String

import logging
log = logging.getLogger(__name__)

class devhome(ListView):
	template_name = 'dev.html'
	model = tax
	#paginate_by = 4
	
	def dispatch(self, request, *args, **kwargs):
		return super(devhome, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(devhome, self).get_queryset()
		self.data=data.filter(status=True).order_by('id')
		return self.data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(devhome, self).get_context_data(*args, **kwargs)
		#context_data.update({'leftmenu': tax.objects.all(),})
		return context_data

		
class devlist(ListView):
	template_name = 'list.html'
	model = goods
	paginate_by = 6
	
	def dispatch(self, request, *args, **kwargs):
		self.tax = get_object_or_404(tax, id=self.kwargs['pk'])
		return super(devlist, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		self.data=super(devlist, self).get_queryset()
		
		#########################################
		########обработка дочерних категорий#####
		#########################################
		datatax=tax.objects.filter(id=self.tax.id).values('id')
		taxin=datatax
		#берем дочернии категории, если есть
		taxparent = tax.objects.filter(parent__in=datatax).values('id')
		if taxparent:
			taxin = taxparent
		#########################################
		
		self.data=self.data.filter(Q(catalogshow=True), Q(status=True), Q(touchscreen=True), Q(tax__in=taxin) | Q(tax__in=datatax)).distinct()
		
		#сортировка
		#sqlalchemy
		#res=goods.sa.query().join(goods.sa.tax).join(propertiesvalue.sa).join(properties.sa).filter(goods.sa.status==True, goods.sa.touchscreen==True, tax.sa.id==12, properties.sa.code=='KOL_RAZ').order_by(cast(propertiesvalue.sa.value, Numeric).desc())
		
		self.data=self.data.order_by('bname')
		
		try:
			self.kwargs['sort']
		except:
			self.data=self.data.order_by('bname')
		else:
			if self.kwargs['sort'] == 'bname':
				self.data=self.data.order_by('bname')
			if self.kwargs['sort'] == 'price':
				self.data=self.data.order_by('price')
			if self.kwargs['sort'] == 'a': #количество зарядов
				self.data=self.data.order_by('propa')
				#self.data=self.data.filter(propertiesvalue__properties__code='KOL_RAZ').annotate(c=Cast('propertiesvalue__value', IntegerField())).order_by('c')
			if self.kwargs['sort'] == 'b': #продолжительность
				self.data=self.data.order_by('propb')
				#self.data=self.data.filter(propertiesvalue__properties__code='TIME').annotate(c=Cast('propertiesvalue__value', IntegerField())).order_by('c')
			
		return self.data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(devlist, self).get_context_data(*args, **kwargs)
		context_data.update({'leftmenu': tax.objects.filter(status=True).order_by('id'),})
		context_data.update({'tax': self.tax,})
		return context_data
		
class Form_filter_devlistsearch(forms.Form):
	q = forms.CharField(label='Поиск', help_text='Введите слово для поиска', widget=forms.TextInput(attrs={'class': 'form-control inputkeyboard','autocomplete': 'off'}), max_length=100, required=False)

class devlistsearch(ListView):
	template_name = 'list_search.html'
	model = goods
	#paginate_by = 6
	
	def dispatch(self, request, *args, **kwargs):
		#self.tax = get_object_or_404(tax, id=self.kwargs['pk'])
		return super(devlistsearch, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
	
		f=Form_filter_devlistsearch(self.request.GET)
		fdata = f.cleaned_data
	
		req = ''
	
		self.data=super(devlistsearch, self).get_queryset()
		
		#########################################
		########обработка дочерних категорий#####
		#########################################
		#datatax=tax.objects.filter(id=self.tax.id).values('id')
		#taxin=datatax
		#берем дочернии категории, если есть
		#taxparent = tax.objects.filter(parent__in=datatax).values('id')
		#if taxparent:
		#	taxin = taxparent
		#########################################
		
		self.data=self.data.filter(Q(catalogshow=True), Q(status=True), Q(touchscreen=True)).distinct()
		
		if f.is_valid():
			#фильтрация
			if fdata['q']:
				req = '%s&q=%s' % (req, fdata['q'])
				self.data=self.data.filter(Q(name__icontains=fdata['q']) | Q(name__search=fdata['q']) | Q(bname__icontains=fdata['q']) | Q(bname__search=fdata['q']))
		
		
		
		self.data=self.data.order_by('bname')
		
		self.req = req
			
		#data=data.order_by('-id')

		#paginator
		self.p = Paginator(self.data, 6)
		#page = self.kwargs['page']
		xpage = self.request.GET.get('xpage', default=1)
		#print self.p.number()
		try:
			pdata = self.p.page(xpage)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			pdata = self.p.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			pdata = self.p.page(self.p.num_pages)
		return pdata
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(devlistsearch, self).get_context_data(*args, **kwargs)
		context_data.update({'form': Form_filter_devlistsearch(self.request.GET),})
		context_data.update({'req': self.req,})
		context_data.update({'urlpage': '/dev/listsearch',})
		context_data.update({'leftmenu': tax.objects.filter(status=True).order_by('id'),})
		#context_data.update({'tax': self.tax,})
		return context_data


	
class devtest(ListView):
	template_name = 'devtest.html'
	model = goods
	#paginate_by = 6
	
	def dispatch(self, request, *args, **kwargs):
		#self.tax = get_object_or_404(tax, id=self.kwargs['pk'])
		return super(devtest, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		self.data=super(devtest, self).get_queryset()

		self.data=self.data.filter(Q(catalogshow=True), Q(status=True), Q(touchscreen=True)).exclude(video__exact='').distinct()
		self.data=self.data.order_by('bname')

		return self.data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(devtest, self).get_context_data(*args, **kwargs)
		return context_data



	
		
class devnovideo(TemplateView):
	template_name = "novideo.html"

	def dispatch(self, request, *args, **kwargs):
		return super(devnovideo, self).dispatch(request, *args, **kwargs)
	
	def get_context_data(self, *args, **kwargs):
		context_data = super(devnovideo, self).get_context_data(*args, **kwargs)
		#context_data.update({'object_list': goods.objects.filter(status=True).order_by('-id')})
		return context_data



		
		
class devp(DetailView):
	model = goods
	template_name = 'p.html'
	
	def dispatch(self, request, *args, **kwargs):
		#self.data = get_object_or_404(self.model, status=True, idbitrix=self.kwargs['pk'])
		self.data = self.model.objects.filter(status=True, idbitrix=self.kwargs['pk'])
		if not self.data.exists():
			return HttpResponseRedirect('/dev/novideo') #если нет товара или с ним какие то проблемы то редирект на novideo
		self.data = self.data.first() #если под одним idbitrix насколько товаров, то берем первый
		return super(devp, self).dispatch(request, *args, **kwargs)
	
	def get_object(self, queryset=None):
		return self.data

	def get_context_data(self, **kwargs):
		context = super(devp, self).get_context_data(**kwargs)
		#context['servername'] = self.data.name
		return context
		
		

#@method_decorator(permission_required('device.add_device'), name='dispatch')
# class devshowvideo(ListView):
	# template_name = 'showvideo.html'
	# model = goods
	# #paginate_by = 50
	
	# def dispatch(self, request, *args, **kwargs):
		# return super(devshowvideo, self).dispatch(request, *args, **kwargs)
		
	# def get_queryset(self):
		# data=super(devshowvideo, self).get_queryset()
		
		# self.data=data.filter(status=True, showondemo=True).order_by('bname')

		# #сортировка
		# try:
			# self.kwargs['sort']
		# except:
			# pass
		# else:
			# if self.kwargs['sort'] == 'bname':
				# self.data=self.data.order_by('bname')
			# if self.kwargs['sort'] == 'price':
				# self.data=self.data.order_by('price')
				
		# #self.a=goods.sa.query()#.filter(goods.sa.status==True, goods.sa.showondemo==True)#.join(propertiesvalue.sa)#.join(properties.sa).filter(properties.sa.status==True)
		# #return a
		
		# return self.data
		
	# def get_context_data(self, *args, **kwargs):
		# context_data = super(devshowvideo, self).get_context_data(*args, **kwargs)
		# #
		# monitorlist=shopset.objects.all()
		# if 'id' in self.request.GET:
			# monitorlist=monitorlist.filter(id=self.request.GET['id'])
		# context_data.update({'monitorlist': monitorlist})
		# #
		# context_data.update({'sortprice': '/dev/showvideo/sort.price'})
		# context_data.update({'sortname': '/dev/showvideo/sort.name'})
		# return context_data
		
		


@csrf_exempt
def devget(request, mac):
	#log.info('start=devget')
	#log.info('mac=%s' % (mac))
	if request.method == 'POST' or request.method == 'GET':
		data = get_object_or_404(device, mac=mac)
		tmp={}
		#настройки магазина
		ss={}
		ss['name']=data.shopset.shop.name
		ss['mixpromo']=data.shopset.mixpromo
		ss['mixaudio']=data.shopset.mixaudio
		ss['promoperiod']=data.shopset.promoperiod
		ss['previewtimeout']=data.shopset.previewtimeout
		ss['radioping']=data.shopset.radioping
		ss['audiopromoperiod']=data.shopset.audiopromoperiod
		#устройство
		dev={}
		dev['name']=data.name
		dev['ip']=data.ip
		dev['mac']=data.mac
		dev['status']=data.status
		dev['videostream']=data.videostream
		dev['audiostream']=data.audiostream
		dev['touchscreen']=data.touchscreen
		dev['radiostream']=data.radiostream
		dev['promovideo']=data.promovideo
		dev['promotouchscreen']=data.promotouchscreen
		dev['updatetime']=data.updatetime
		dev['starturl']=data.starturl
		dev['audiocatalog']=data.audiocatalog
		dev['videocatalog']=data.videocatalog
		dev['promocatalog']=data.promocatalog
		dev['catalogserverurl']=data.catalogserverurl
		
		#playlist
		pl={}
		pl['source']=False
		pl['type']=False
		if data.shopset.playlist:
			if data.shopset.playlist.status == True:
				pl['source']=data.shopset.playlist.url
				pl['type']=data.shopset.playlist.type
		
		#
		tmp['shop']=ss
		tmp['device']=dev
		tmp['playlist']=pl

		

		
		tmp={'res': 1, 'data': tmp}
		return HttpResponse(json.dumps(tmp), content_type='application/json')
		
	tmp={'res': 0, 'data': u'Ошибка',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')
		
		

		
		
	
@csrf_exempt
def devsetip(request, mac):
	log.info('start=devsetip')
	log.info('mac=%s' % (mac))
	if request.method == 'GET' and 'ip' in request.GET and 'crc' in request.GET:
		crc = makeapitoken(mac)
		if crc == request.GET['crc']:
			data = get_object_or_404(device, mac=mac)
			data.ip = request.GET['ip']
			data.pingsetip = datetime.datetime.now()
			data.save()
			tmp={'res': 1, 'data': u'set ip good',}
			return HttpResponse(json.dumps(tmp), content_type='application/json')
		
	tmp={'res': 0, 'data': u'bad',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')
				
		
		
@csrf_exempt
def devping(request, mac):
	#log.info('start=devping')
	#log.info('mac=%s' % (mac))
	if request.method == 'GET' and 'crc' in request.GET:
		crc = makeapitoken(mac)
		if crc == request.GET['crc']:
			data = get_object_or_404(device, mac=mac)
			data.pingcron = datetime.datetime.now()
			REBOOT=data.reboot #device must reboot
			data.reboot = False
			data.save()
			tmp={'res': 1, 'data': u'ping good', 'reboot': REBOOT, }
			return HttpResponse(json.dumps(tmp), content_type='application/json')
		
	tmp={'res': 0, 'data': u'bad',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')
				
	


@csrf_exempt
def dev_os_system(request, mac):
	#log.info('start=devping')
	#log.info('mac=%s' % (mac))
	if request.method == 'GET' and 'crc' in request.GET:
		crc = makeapitoken(mac)
		if crc == request.GET['crc']:
			data = get_object_or_404(device, mac=mac)
			command=data.os_system #сначало забираем команду
			data.os_system = '' #потом ее удаляем
			data.save() #записываем результат
			tmp={'res': 1, 'data': u'dev_os_system OK', 'os_system': command, } #в последнию очередь отправляем команду устройсту
			return HttpResponse(json.dumps(tmp), content_type='application/json')
		
	tmp={'res': 0, 'data': u'bad',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')
	

@csrf_exempt
def devnull(request, mac):
	log.info('start=devnull')
	log.info('mac=%s' % (mac))
	log.info('ip=%s' % (request.GET['ip']))
	if request.method == 'GET' and 'ip' in request.GET and 'crc' in request.GET:
		crc = makeapitoken(mac)
		if crc == request.GET['crc']:
			tmp={'res': 1, 'data': u'devnull',}
			return HttpResponse(json.dumps(tmp), content_type='application/json')
		
	tmp={'res': 0, 'data': u'bad',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')
						
		
		


@csrf_exempt
def devdemolist(request):
	if request.method == 'POST' or request.method == 'GET':
		data = goods.objects.filter(status=True, showondemo=True)
		if data.exists():
			tmpdata = []
			for i in data:
				tmpdata.append({'status': i.status, 'name': i.name, 'idbitrix': i.idbitrix, 'video': i.videomp4,})
			tmp={'res': 1, 'data': tmpdata}
			return HttpResponse(json.dumps(tmp), content_type='application/json')
		
	tmp={'res': 0, 'data': u'Ошибка',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')


@csrf_exempt
def devmedialist(request):
	if request.method == 'POST' or request.method == 'GET':
		data = media.objects.all()
		if data.exists():
			tmpdata = []
			for i in data:
				tmpdata.append({'id': i.id, 'name': i.name, 'file': i.file, 'format': i.format, 'audio': i.audio, 'promo': i.promo, 'instruction': i.instruction, 'advertising': i.advertising, 'duration': i.duration,})
			tmp={'res': 1, 'data': tmpdata}
			return HttpResponse(json.dumps(tmp), content_type='application/json')
		
	tmp={'res': 0, 'data': u'Ошибка',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')
	
	
	
	
class devcountdebug(TemplateView):
	template_name = "count.html"
	

	
	
@csrf_exempt
def devsetcountvisitor(request, mac):
	# if request.method == 'GET' and 'crc' in request.GET:
		# crc = makeapitoken(mac)
		# print crc, request.GET['crc']
		# if crc == request.GET['crc']:
			# data = get_object_or_404(device, mac=mac)
			# c=countvisitor.objects.create(shop=data.shopset.shop, type=request.GET['type'])
			# c.save()
			# tmp={'res': 1, 'data': u'set count good',}
			# return HttpResponse(json.dumps(tmp), content_type='application/json')
	if request.method == 'POST' and 'crc' in request.POST:
		crc = makeapitoken(mac)
		#print crc, request.POST['crc'], request.FILES
		if crc == request.POST['crc']:
			data = get_object_or_404(device, mac=mac)
			c=countvisitor.objects.create(shop=data.shopset.shop, video=request.FILES['video'], minface=request.POST['minface'], maxface=request.POST['maxface'], mineye=request.POST['mineye'], maxeye=request.POST['maxeye'])
			if 'zip' in request.FILES:
				c.zip=request.FILES['zip']
			c.save()
			tmp={'res': 1, 'data': u'set count good',}
			return HttpResponse(json.dumps(tmp), content_type='application/json')
		
	tmp={'res': 0, 'data': u'bad',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')

	
	
	
	
@csrf_exempt
def devsendvideo(request, mac):
	if request.method == 'POST' and 'crc' in request.POST:
		crc = makeapitoken(mac)
		#print crc, request.POST['crc'], request.FILES
		if crc == request.POST['crc']:
			data = get_object_or_404(device, mac=mac)
			c=countvisitor.objects.create(shop=data.shopset.shop, video=request.FILES['video'])
			c.save()
			tmp={'res': 1, 'data': u'set count good',}
			return HttpResponse(json.dumps(tmp), content_type='application/json')
		
	tmp={'res': 0, 'data': u'bad',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')
	



@csrf_exempt
def devkondor(request, salt, crc):
	if request.method == 'POST' or request.method == 'GET':
		tmp={'res': 0, 'data': u'bad',}
		#
		mycrc = makeapitoken(salt)
		if crc != mycrc:
			tmp={'res': 0, 'data': u'bad token or crc',}
			return HttpResponse(json.dumps(tmp), content_type='application/json')
		#
		data = request.body
		try:
			data = json.loads(data)
			data = json.loads(data)
			#print '==', type(data), data
		except:
			pass
		else:
			try:
				d=device.objects.get(mac=data['msg']['@num'])
			except:
				pass
			else:
				#print d.mac
				#print data['msg']['@dev'], data['msg']['@num'], data['msg']['@time'], data['msg']['@event'], data['msg']['@entry'], data['msg']['@exit']
				
				#print data['msg']['@time']
				
				try:
					ctime=datetime.datetime.strptime(data['msg']['@time'],"%d.%m.%y %H:%M:%S")
				except:
					ctime=None
				#print ctime
				
				c=countvisitor.objects.create(shop=d.shopset.shop, event=data['msg']['@event'], name='%s_%s' % (data['msg']['@dev'], data['msg']['@num']), info=request.body, counttime=ctime)
				c.save()

				tmp={'res': 1, 'data': u'set count good',}

	return HttpResponse(json.dumps(tmp), content_type='application/json')
	
	
	
	
	
#@method_decorator(permission_required('device.add_device'), name='dispatch')
class devcontrollist(ListView):
	template_name = 'devcontrollist.html'
	model = shopset
	#paginate_by = 1
	
	def dispatch(self, request, *args, **kwargs):
		return super(devcontrollist, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(devcontrollist, self).get_queryset()
		data=data.filter(device__status=True, shop__profileuser__user=self.request.user).distinct()
		
		#
		# paging = self.request.GET.get('paging', self.paginate_by)
		# try:
			# int(paging)
		# except:
			# pass
		# else:
			# self.paginate_by = paging
		# #
		
		# if 'pagnum' not in self.request.session:
			# self.request.session['pagnum'] = 1
		
		# try:
			# pagnum = int(self.request.GET.get('pagnum', 1))
		# except:
			# pass
		# else:
			# self.request.session['pagnum'] = pagnum
			

		# pagnum = int(self.request.session.get('pagnum'))
		
		# paginator = Paginator(data, pagnum)

		# page = self.request.GET.get('page', 1)
		# data = paginator.page(2)
		# try:
			# data = paginator.page(page)
		# except PageNotAnInteger:
			# data = paginator.page(1)
		# except EmptyPage:
			# data = paginator.page(paginator.num_pages)
		
		
		return data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(devcontrollist, self).get_context_data(*args, **kwargs)
		#context_data.update({'sortprice': '/dev/showvideo/sort.price'})
		return context_data
	
@csrf_exempt
def devreboot(request, pk):
	if request.method == 'GET':
		d = get_object_or_404(device, id=pk, status=True, reboot=False,	 shopset__shop__profileuser__user=request.user)
		d.reboot = True
		d.save()
		return HttpResponseRedirect('/dev/control/list')
	return HttpResponseRedirect('/dev/control/list')
	

	
	
	
	
	
	
#для тестов, удалить
class devlist1(ListView):
	template_name = 'list1.html'
	model = goods
	paginate_by = 8
	
	def dispatch(self, request, *args, **kwargs):
		self.tax = get_object_or_404(tax, id=self.kwargs['pk'])
		return super(devlist1, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(devlist1, self).get_queryset()
		
		#########################################
		########обработка дочерних категорий#####
		#########################################
		datatax=tax.objects.filter(id=self.tax.id).values('id')
		taxin=datatax
		#берем дочернии категории, если есть
		taxparent = tax.objects.filter(parent__in=datatax).values('id')
		if taxparent:
			taxin = taxparent
		#########################################
		
		self.data=data.filter(status=True, touchscreen=True, tax__in=taxin).distinct()
		
		#сортировка
		#sqlalchemy
		#res=goods.sa.query().join(goods.sa.tax).join(propertiesvalue.sa).join(properties.sa).filter(goods.sa.status==True, goods.sa.touchscreen==True, tax.sa.id==12, properties.sa.code=='KOL_RAZ').order_by(cast(propertiesvalue.sa.value, Numeric).desc())
		
		try:
			self.kwargs['sort']
		except:
			self.data=self.data.order_by('name')
		else:
			if self.kwargs['sort'] == 'name':
				self.data=self.data.order_by('name')
			if self.kwargs['sort'] == 'price':
				self.data=self.data.order_by('price')
			if self.kwargs['sort'] == 'a': #количество зарядов
				self.data=self.data.order_by('propa')
				#self.data=self.data.filter(propertiesvalue__properties__code='KOL_RAZ').annotate(c=Cast('propertiesvalue__value', IntegerField())).order_by('c')
			if self.kwargs['sort'] == 'b': #продолжительность
				self.data=self.data.order_by('propb')
				#self.data=self.data.filter(propertiesvalue__properties__code='TIME').annotate(c=Cast('propertiesvalue__value', IntegerField())).order_by('c')
			
		return self.data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(devlist1, self).get_context_data(*args, **kwargs)
		context_data.update({'leftmenu': tax.objects.filter(status=True).order_by('id'),})
		context_data.update({'tax': self.tax,})
		return context_data
		
	
@csrf_exempt
def devshowvideocount(request, pk):
	if request.method == 'GET':
		data = get_object_or_404(goods, id=pk)
		data.showvideocount = data.showvideocount+1
		data.save()
		tmp={'res': 1, 'data': u'count',}
		return HttpResponse(json.dumps(tmp), content_type='application/json')
		
	tmp={'res': 0, 'data': u'bad',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')
	