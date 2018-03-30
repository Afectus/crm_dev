from .models import *
from django.views.generic.edit import CreateView, DeleteView, UpdateView ,FormView
from django.views.generic import ListView,DetailView
from django.urls import reverse_lazy,reverse
from django.shortcuts import get_object_or_404
from acl.views import get_object_or_denied
from django.shortcuts import HttpResponseRedirect
from django import forms


class Form_filter_order(forms.Form):

	sortchoice=(
		('ctime', 'Новые'),
		('-ctime', 'Старые'),
		('-area', 'Район'),
		('-status', 'Статус'),
		)
	
	sort = forms.ChoiceField(label='Сортировка', help_text='Сортировать по полю', widget=forms.Select(attrs={'class': 'form-control'}), choices=sortchoice, required=False)


class dellist_list(ListView):
	model = dellist
	template_name = 'dellist_list.html'
	paginate_by = 10

	
	def dispatch(self, request, *args, **kwargs):
		#get_object_or_denied(self.request.user, 'deliveryapp', 'L') #проверяем права
		return super(dellist_list, self).dispatch(request, *args, **kwargs)
	
	def get_queryset(self):
		data = super(dellist_list, self).get_queryset().order_by('-id')

		f=Form_filter_order(self.request.GET)
		req = ''
		
		if f.is_valid():
			fdata = f.cleaned_data
			if fdata['sort']:
				data=data.order_by(fdata['sort'])
		
		return data

	def get_context_data(self, *args, **kwargs):
		context_data = super(dellist_list, self).get_context_data(*args, **kwargs)
		context_data.update({'form': Form_filter_order(self.request.GET),})
		return context_data

class dellist_mylist(ListView):
	model = dellist
	template_name = 'dellist_mylist.html'
	paginate_by = 10
	
	def dispatch(self, request, *args, **kwargs):
		#get_object_or_denied(self.request.user, 'deliveryapp', 'L') #проверяем права
		return super(dellist_mylist, self).dispatch(request, *args, **kwargs)

	def get_queryset(self):
		data = super(dellist_mylist, self).get_queryset()
		data = data.filter(courier=self.request.user).order_by('-id')

		f=Form_filter_order(self.request.GET)
		req = ''
		
		if f.is_valid():
			fdata = f.cleaned_data
			if fdata['sort']:
				data=data.order_by(fdata['sort'])
		return data

	def get_context_data(self, *args, **kwargs):
		context_data = super(dellist_mylist, self).get_context_data(*args, **kwargs)
		context_data.update({'form': Form_filter_order(self.request.GET),})
		return context_data


class dellist_detail(DetailView):
	model = dellist
	template_name = 'dellist_detail.html'

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'deliveryapp', 'L') #проверяем права
		return super(dellist_detail, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context_get_delevent = delevent.objects.filter(dellist=self.kwargs['pk'])
		context_data = super(dellist_detail, self).get_context_data(**kwargs)
		context_data.update({'context_get_delevent': context_get_delevent})
		return context_data


class dellist_add(CreateView):
	model = dellist
	template_name = '_edit2.html'
	fields = ['order', 'status' ,'area', 'addr', 'comment']

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'deliveryapp', 'C') #проверяем права
		return super(dellist_add, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.save()
		self.data=instance
		comments = "%s создал доставку id: %s" % (self.request.user, instance.id)
		de=delevent.objects.create(user=self.request.user, dellist=instance, event='add', comment=comments,)
		return super(dellist_add, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('dellist_list')


class dellist_edit(UpdateView):
	model = dellist
	template_name = '_edit2.html'
	fields = ['order', 'status' ,'area', 'addr', 'comment']

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.save()
		self.data=instance
		comments = "%s отредактировал доставку id: %s" % (self.request.user, instance.id)
		de=delevent.objects.create(user=self.request.user, dellist=instance, event='edit', comment=comments,)
		return super(dellist_edit, self).form_valid(form)

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'deliveryapp', 'C') #проверяем права
		return super(dellist_edit, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return reverse_lazy('dellist_list')

def dellist_accept(request, pk):
	data = get_object_or_404(dellist, id=pk, status='wait')
	#get_object_or_denied(request.user, 'deliveryapp', 'C')
	data.status='accept'
	data.courier=request.user
	data.save()
	comments = "%s взял доставку id: %s"%(request.user, data.id)
	de=delevent.objects.create(user=request.user, dellist=data, event='accept', comment=comments,)
	return HttpResponseRedirect(reverse('dellist_detail', args=[data.id]))

def dellist_success(request, pk):
	data = get_object_or_404(dellist, id=pk, status='accept')
	#get_object_or_denied(request.user, 'deliveryapp', 'C')
	data.status='success'
	data.save()
	comments = "%s выполнил доставку id: %s"%(request.user, data.id)
	de=delevent.objects.create(user=request.user, dellist=data, event='success', comment=comments,)
	return HttpResponseRedirect(reverse('dellist_detail', args=[data.id]))


