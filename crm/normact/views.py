# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse
from django.http import Http404
from django.contrib.auth.models import User

import time
import requests
import datetime
from django.utils import timezone
# Create your views here.
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView

from django.views.generic import DetailView, DeleteView
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView

from dj.views import *
from acl.views import *
from .models import *
from django.urls import reverse

# grantchoice=(('L', 'Список'), ('R', 'Чтение'), ('С', 'Создание'), ('U', 'Редактирование'),)

class normact_add(CreateView):
    model = normact
    template_name = 'normact_add.html'
    fields = ['user', 'file', 'choice', 'name', 'comment']

    def dispatch(self, request, *args, **kwargs):
        get_object_or_denied(self.request.user, 'normact', 'C')
        return super(normact_add, self).dispatch(request, *args, **kwargs)

    # def form_valid(self, form):
    #     instance = form.save(commit=False)
    #     # instance.user = self.request.user
    #     instance.save()
    #     return super(normact_add, self).form_valid(form)

    def get_success_url(self):
        return reverse('normact:normact_list')

class normact_list(ListView): 
    template_name = 'normact_list.html' 
    model = normact
    # paginate_by = 6

    def dispatch(self, request, *args, **kwargs):
        get_object_or_denied(self.request.user, 'normact', 'L')
        return super(normact_list, self).dispatch(request, *args, **kwargs) 

    def get_queryset(self):
        data=super(normact_list, self).get_queryset()
        if 'type' in self.request.GET:
            data=data.filter(choice=self.request.GET['type'])
        return data

class normact_edit(UpdateView):
    model = normact
    template_name = 'normact_add.html'
    fields = ['user', 'file', 'choice', 'name', 'comment']
   
    def dispatch(self, request, *args, **kwargs):
        get_object_or_denied(self.request.user, 'normact', 'L')
        return super(normact_edit, self).dispatch(request, *args, **kwargs)

    # def get_object(self, queryset=None):
    #     return get_object_or_denied(self.request.user, 'normact', 'U')

    def get_success_url(self):
        return reverse('normact:normact_list')


class normact_del(DeleteView): 
    template_name = '_confirm_delete.html' 
    model = normact

    def dispatch(self, request, *args, **kwargs):
        get_object_or_denied(self.request.user, 'normact', 'U')
        return super(normact_del, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(normact_del, self).get_context_data(**kwargs)
        context['msg'] = u'Вы уверены что хотите удалить '
        context['back_url'] = reverse('normact:normact_list')
        return context

    def get_success_url(self):
        return reverse('normact:normact_list')
