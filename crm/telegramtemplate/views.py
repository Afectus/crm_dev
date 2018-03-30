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

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator

from dj.views import *
from .models import *
from notify.models import *
from django.urls import reverse


# class telegramtemplate_add(CreateView):
#     model = telegramtemplate
#     template_name = 'telegramtemplate_add.html'
#     fields = ['name', 'message']

#     def form_valid(self, form):
#         instance = form.save(commit=False)
#         instance.save()
#         return super(telegramtemplate_add, self).form_valid(form)

#     def get_success_url(self):
#         return reverse('telegramtemplate:telegramtemplate_list')


@method_decorator(permission_required('telegramtemplate.add_telegramtemplate'), name='dispatch')
class telegramtemplate_list(ListView): 
    template_name = 'telegramtemplate_list.html' 
    model = telegramtemplate


	
@method_decorator(permission_required('telegramtemplate.add_telegramtemplate'), name='dispatch')
class telegramtemplate_edit(UpdateView):
    model = telegramtemplate
    template_name = 'telegramtemplate_add.html'
    fields = ['message']
   
    def get_success_url(self):
        return reverse('telegramtemplate:telegramtemplate_list')
