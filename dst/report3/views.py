from django.shortcuts import render
from django.core.paginator import Paginator

from django.views.generic import ListView
from django.views.generic.edit import CreateView,UpdateView
from django.urls import reverse_lazy
from node.models import *
from .models import *
from acl.views import get_object_or_denied

#добавить сумму всех элементов
class list_ostatkisklad(ListView):
	model = goodsinstock
	#model = Paginatornumm
	template_name = 'list_ostatkisklad.html'
	#fields = ['paginatornumm']
	context_object_name = 'goodsinstockk'
	#paginate_by = 10
	
		
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'list_ostatkisklad', 'L') #проверяем права
		return super(list_ostatkisklad, self).dispatch(request, *args, **kwargs)

	def get_queryset(self):
		data = super(list_ostatkisklad, self).get_queryset()
		data = data.filter(value__gt = 0).order_by('goods')
		# Проверяем возможна ли вообще пагинация
		if len(data) > 2:
			if 'pagnum' not in self.request.session:
				self.request.session['pagnum'] = len(data) - 1

			try:
				pagnum = int(self.request.GET.get('pagnum'))
			except:
				pass
			else:
				self.request.session['pagnum'] = pagnum

			pagnum = int(self.request.session.get('pagnum'))

			if pagnum >= len(data):
				pagnum = len(data) - 1
				self.request.session['pagnum'] = len(data) - 1
			elif pagnum <= 0:
				pagnum = len(data) - 1
				self.request.session['pagnum'] = len(data) - 1

			paginator = Paginator(data, abs(pagnum))
			page = self.request.GET.get('page', 1)

			try:
				data = paginator.page(page)
			except PageNotAnInteger:
				data = paginator.page(1)
			except EmptyPage:
				data = paginator.page(paginator.num_pages)

			return data
		else:
			return data

"""
	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		instance.save()
		self.data = instance
		return super(list_ostatkisklad, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('check_detail')

	def get_context_data(self, **kwargs):
		goodsinstockk = goodsinstock.objects.filter(value__gt = 0).order_by('goods')
		getpaginatornumm = Paginatornumm.objects.filter(user=self.request.user)
		#print('-_-' * 50)
		#print(len(getpaginatornumm))
		page = self.request.GET.get('page', 1)

		try:
			pagnum = getpaginatornumm[0].paginatornumm
		except IndexError:
			pagnum = 50

		try:
			int(pagnum)
		except TypeError:
			pagnum = 50


		paginator = Paginator(goodsinstockk, pagnum)
	  
		try:
			goodsinstockk = paginator.page(page)
		except PageNotAnInteger:
			goodsinstockk = paginator.page(1)
		except EmptyPage:
		   goodsinstockk = paginator.page(paginator.num_pages)

		context_data = super(list_ostatkisklad, self).get_context_data(**kwargs)
		context_data.update({'goodsinstockk': goodsinstockk})
		context_data.update({'getpaginatornumm': getpaginatornumm})
		return context_data

class paginatornumm_update(UpdateView):
	model = Paginatornumm
	template_name = 'update_paginator.html'
	fields = ['paginatornumm']

	def get_success_url(self):
		return reverse_lazy('check_detail')
"""