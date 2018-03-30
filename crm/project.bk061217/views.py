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
from .models import *
from notify.models import *
from django.urls import reverse

class project_add(CreateView):
    model = project
    template_name = '_edit2.html'
    fields = ['name', 'desc', 'executor', 'plansum']
    # success_url = reverse('project:project_list')

    # def dispatch(self, request, *args, **kwargs):
    #     self.data = get_object_or_404(project, user=self.request.user)
    #     return super(project_detail, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        self.data = instance
        return super(project_add, self).form_valid(form)

    def get_success_url(self):
        #send telegram
        path_project = reverse('project:project_detail',args=[self.data.id])
        today = datetime.date.today()
        value_user = u'Поздравляю! Сегодня %s вы создали новый проект %s (ссылка: crm.babah24.ru%s)' % (today, self.data.name, path_project)
        value_chat = u'Сегодня %s пользователем %s был создан проект %s (ссылка: crm.babah24.ru%s)' % (today, self.data.user, self.data.name, path_project)

        nh=notifyhandler.objects.get(name='telegram')
        
        # send to user
        try:
            nuk=notifyuserkey.objects.get(user=self.data.user, handler=nh)
        except:
            pass
        else: 
            nq=notifyqueue.objects.create(user=self.data.user, handler=nh, value=value_user)
        # send to telegram_chat
        try:
             telegram_chat_user = User.objects.get(username='telegram_chat')
        except:
             pass
        else:
             nq=notifyqueue.objects.create(user=telegram_chat_user, handler=nh, value=value_chat)
        # send to executors
        for e in self.data.executor.all().exclude(user=self.data.user):
            value_executor = u'Сегодня %s вас добавили в новый проект %s (ссылка: crm.babah24.ru%s)' % (today, self.data.name, path_project)
            try:
                nuk=notifyuserkey.objects.get(user=e.user, handler=nh)
            except:
                pass
            else: 
                nq=notifyqueue.objects.create(user=e.user, handler=nh, value=value_executor)
        
        return reverse('project:project_list')

#@method_decorator(permission_required('worktask.add_usertask'), name='dispatch') 
class project_list(ListView): 
    template_name = 'project_list.html' 
    model = project 
    paginate_by = 6

    def dispatch(self, request, *args, **kwargs): 
        return super(project_list, self).dispatch(request, *args, **kwargs) 

    def get_queryset(self): 
        data=super(project_list, self).get_queryset() 
        # data = data.filter(user=self.request.user) #for get_context_data 
        return data 

class project_edit(UpdateView):
    model = project
    template_name = '_edit2.html'
    fields = ['name', 'status', 'desc', 'executor', 'plansum']
    #success_url = reverse('project:project_list')

#     def dispatch(self, request, *args, **kwargs):
#         get_object_or_404(self.model, status='created', id=self.kwargs['pk'], user=request.user)
#         return super(project_edit, self).dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        self.data=super(project_edit, self).get_object()
        if self.data.user != self.request.user:
            raise PermissionDenied
        return self.data

    def get_success_url(self):
        path_project = reverse('project:project_detail',args=[self.data.id])
        today = datetime.date.today()
        nh=notifyhandler.objects.get(name='telegram')

        if self.data.status == 'archived':
            #send telegram
            value_user = u'Сегодня %s вы отправили проект %s в архив (ссылка: crm.babah24.ru%s)' % (today, self.data.name, path_project)
            value_chat = u'Сегодня %s пользователем %s проект %s был переведен в архив (ссылка: crm.babah24.ru%s)' % (today, self.data.user, self.data.name, path_project)

            # send to user
            try:
                nuk=notifyuserkey.objects.get(user=self.data.user, handler=nh)
            except:
                pass
            else: 
                nq=notifyqueue.objects.create(user=self.data.user, handler=nh, value=value_user)
            # send to telegram_chat
            try:
                telegram_chat_user = User.objects.get(username='telegram_chat')
            except:
                pass
            else:
                nq=notifyqueue.objects.create(user=telegram_chat_user, handler=nh, value=value_chat)
            # send to executors
            for e in self.data.executor.all().exclude(user=self.data.user):
                value_executor = u' Сегодня %s проект %s, в котором вы участвуете, был переведен в архив (ссылка: crm.babah24.ru%s)' % (today, self.data.name, path_project)
                try:
                    nuk=notifyuserkey.objects.get(user=e.user, handler=nh)
                except:
                    pass
                else: 
                    nq=notifyqueue.objects.create(user=e.user, handler=nh, value=value_executor)
            
        else:     
            #send telegram
            value_user = u'Сегодня %s проект %s был вами изменён (ссылка: crm.babah24.ru%s)' % (today, self.data.name, path_project)
            value_chat = u'Сегодня %s пользователем %s проект %s был изменён (ссылка: crm.babah24.ru%s)' % (today, self.data.user, self.data.name, path_project)     
            # send to user
            try:
                nuk=notifyuserkey.objects.get(user=self.data.user, handler=nh)
            except:
                pass
            else: 
                nq=notifyqueue.objects.create(user=self.data.user, handler=nh, value=value_user)
            # send to telegram_chat
            try:
                telegram_chat_user = User.objects.get(username='telegram_chat')
            except:
                pass
            else:
                nq=notifyqueue.objects.create(user=telegram_chat_user, handler=nh, value=value_chat)
            # send to executors
            for e in self.data.executor.all().exclude(user=self.data.user):
                value_executor = u' Сегодня %s проект %s, в котором вы участвуете, был изменён (ссылка: crm.babah24.ru%s)' % (today, self.data.name, path_project)
                try:
                    nuk=notifyuserkey.objects.get(user=e.user, handler=nh)
                except:
                    pass
                else: 
                    nq=notifyqueue.objects.create(user=e.user, handler=nh, value=value_executor)

        return path_project

class project_detail(CreateView): 
    template_name = 'project_detail.html' 
    model = projectcomment
    fields = ['value']

    def dispatch(self, request, *args, **kwargs):
        self.data = get_object_or_404(project, id=self.kwargs['pk'])
        return super(project_detail, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        # instance.project = self.data
        instance.save()
        self.data.projectcomment.add(instance)

        #send telegram
        path_project = reverse('project:project_detail',args=[self.data.id])
        today = datetime.date.today()
        value_user = u'Сегодня %s пользователь %s оставил комментарий для проекта %s (ссылка: crm.babah24.ru%s)' % (today, self.request.user, self.data.name, path_project)
        value_chat = u'Сегодня %s пользователь %s оставил комментарий для проекта %s (ссылка: crm.babah24.ru%s)' % (today, self.request.user, self.data.name, path_project)

        nh=notifyhandler.objects.get(name='telegram')

        try:
            nuk=notifyuserkey.objects.get(user=self.data.user, handler=nh)
        except:
            pass
        else: 
            nq=notifyqueue.objects.create(user=self.data.user, handler=nh, value=value_user)

        try:
             telegram_chat_user = User.objects.get(username='telegram_chat')
        except:
             pass
        else:
             nq=notifyqueue.objects.create(user=telegram_chat_user, handler=nh, value=value_chat)

        for e in self.data.executor.all().exclude(user=self.data.user):
            value_executor = u'Сегодня %s пользователь %s оставил комментарий для проекта %s (ссылка: crm.babah24.ru%s)' % (today, self.request.user, self.data.name, path_project)
            try:
                nuk=notifyuserkey.objects.get(user=e.user, handler=nh)
            except:
                pass
            else: 
                nq=notifyqueue.objects.create(user=e.user, handler=nh, value=value_executor)

        return super(project_detail, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context_data = super(project_detail, self).get_context_data(*args, **kwargs)
        context_data.update({'object': self.data,})
        return context_data

    def get_success_url(self):
        return reverse('project:project_detail',args=[self.data.id])

class project_pict_add(CreateView): 
    template_name = 'project_file_add.html'
    fields = ['pict', 'desc']
    model = projectpict

    def dispatch(self, request, *args, **kwargs):
        self.data = get_object_or_404(project, id=self.kwargs['pk'], user=self.request.user)
        return super(project_pict_add, self).dispatch(request, *args, **kwargs)
    
    # def get_form(self, form_class=None):
    #     if form_class is None:
    #         form_class = self.get_form_class()
    #         form = super(project_pict_add, self).get_form(form_class)
    #         form.fields['desc'].initial='asd'
    #     return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        # instance.project. = self.data
        instance.save()
        self.data.pict.add(instance)
        return super(project_pict_add, self).form_valid(form)

    def get_success_url(self):
        return reverse('project:project_detail',args=[self.data.id])

class project_pict_del(DeleteView): 
    template_name = '_confirm_delete.html' 
    model = projectpict

    def dispatch(self, request, *args, **kwargs):
        return super(project_pict_del, self).dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        self.data=super(project_pict_del, self).get_object()
        if self.data.project_set.all().first().user != self.request.user:
            raise PermissionDenied
        return self.data
    
    def get_context_data(self, **kwargs):
        context = super(project_pict_del, self).get_context_data(**kwargs)
        context['msg'] = u'Вы уверены что хотите удалить '
        context['back_url'] = reverse('project:project_detail',args=[self.data.project_set.all().first().id])
        return context

    def get_success_url(self):
        return reverse('project:project_detail',args=[self.data.project_set.all().first().id])

class project_file_add(CreateView): 
    template_name = 'project_file_add.html'
    fields = ['sourcefile', 'desc']
    model = projectfile

    def dispatch(self, request, *args, **kwargs):
        self.data = get_object_or_404(project, id=self.kwargs['pk'], user=self.request.user)
        return super(project_file_add, self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        self.data.file.add(instance)
        return super(project_file_add, self).form_valid(form)

    def get_success_url(self):
        return reverse('project:project_detail',args=[self.data.id])

class project_file_del(DeleteView): 
    template_name = '_confirm_delete.html'
    model = projectfile

    def dispatch(self, request, *args, **kwargs):
        return super(project_file_del, self).dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        self.data=super(project_file_del, self).get_object()
        if self.data.project_set.all().first().user != self.request.user:
            raise PermissionDenied
        return self.data

    def get_context_data(self, **kwargs):
        context = super(project_file_del, self).get_context_data(**kwargs)
        context['msg'] = u'Вы уверены что хотите удалить '
        context['back_url'] = reverse('project:project_detail',args=[self.data.project_set.all().first().id])
        return context


    def get_success_url(self):
        return reverse('project:project_detail',args=[self.data.project_set.all().first().id])

class projectcomment_edit(UpdateView):
    model = projectcomment
    template_name = '_edit2.html'
    fields = ['value']

    def dispatch(self, request, *args, **kwargs):
        return super(projectcomment_edit, self).dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        self.data=super(projectcomment_edit, self).get_object()
        if self.data.user != self.request.user:
            raise PermissionDenied
        return self.data

    def get_success_url(self):
        return reverse('project:project_detail',args=[self.data.project_set.all().first().id])

class projectcomment_del(DeleteView): 
    template_name = '_confirm_delete.html' 
    model = projectcomment

    def dispatch(self, request, *args, **kwargs):
        return super(projectcomment_del, self).dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        self.data=super(projectcomment_del, self).get_object()
        if self.data.user != self.request.user:
            raise PermissionDenied
        return self.data
    
    def get_context_data(self, **kwargs):
        context = super(projectcomment_del, self).get_context_data(**kwargs)
        context['msg'] = u'Вы уверены что хотите удалить '
        context['back_url'] = reverse('project:project_detail',args=[self.data.project_set.all().first().id])
        return context

    def get_success_url(self):
        return reverse('project:project_detail',args=[self.data.project_set.all().first().id])

class projectcomment_pict_add(CreateView):
    model = projectpict
    template_name = 'project_file_add.html'
    fields = ['pict', 'desc']
#     #success_url = '/project/list/'

    def dispatch(self, request, *args, **kwargs):
        self.comment = get_object_or_404(projectcomment, id=self.kwargs['pk'], user=request.user)
        return super(projectcomment_pict_add, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.projectcomment = self.comment
        instance.save()
        self.comment.pict.add(instance)
        return super(projectcomment_pict_add, self).form_valid(form)

    def get_success_url(self):
        return reverse('project:project_detail',args=[self.comment.project_set.all().first().id])

class projectcomment_pict_del(DeleteView):
    model = projectpict
    template_name = '_confirm_delete.html'
    
    def dispatch(self, request, *args, **kwargs):
        return super(projectcomment_pict_del, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        self.data=super(projectcomment_pict_del, self).get_object()
        if self.data.projectcomment_set.all().first().user != self.request.user:
            raise PermissionDenied
        return self.data
    
    def get_context_data(self, **kwargs):
        context = super(projectcomment_pict_del, self).get_context_data(**kwargs)
        context['msg'] = u'Вы уверены что хотите удалить '
        context['back_url'] = reverse('project:project_detail',args=[self.data.projectcomment_set.all().first().project_set.all().first().id])
        return context

    def get_success_url(self):
        return reverse('project:project_detail',args=[self.data.projectcomment_set.all().first().project_set.all().first().id])

class projectcomment_file_add(CreateView): 
    template_name = 'project_file_add.html' 
    model = projectfile
    fields = ['sourcefile', 'desc']

    def dispatch(self, request, *args, **kwargs):
        self.comment = get_object_or_404(projectcomment, id=self.kwargs['pk'], user=request.user)
        return super(projectcomment_file_add, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.projectcomment = self.comment
        instance.save()
        self.comment.file.add(instance)
        return super(projectcomment_file_add, self).form_valid(form)

    def get_success_url(self):
        return reverse('project:project_detail',args=[self.comment.project_set.all().first().id])

class projectcomment_file_del(DeleteView): 
    template_name = '_confirm_delete.html' 
    model = projectfile

    def dispatch(self, request, *args, **kwargs):
        return super(projectcomment_file_del, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        self.data=super(projectcomment_file_del, self).get_object()
        if self.data.projectcomment_set.all().first().user != self.request.user:
            raise PermissionDenied
        return self.data

    def get_context_data(self, **kwargs):
        context = super(projectcomment_file_del, self).get_context_data(**kwargs)
        context['msg'] = u'Вы уверены что хотите удалить '
        context['back_url'] = reverse('project:project_detail',args=[self.data.projectcomment_set.all().first().project_set.all().first().id])
        return context

    def get_success_url(self):
        return reverse('project:project_detail',args=[self.data.projectcomment_set.all().first().project_set.all().first().id])

################# projectstep ################

class projectstep_add(CreateView):
    model = projectstep
    template_name = '_edit2.html'
    fields = ['projectstep', 'name', 'executor', 'distributor', 'edate', 'desc']
#     success_url = reverse('project:project_list'),comment 

    def dispatch(self, request, *args, **kwargs):
        self.p = get_object_or_404(project, id=self.kwargs['pk'], user=self.request.user)
        return super(projectstep_add, self).dispatch(request, *args, **kwargs)
    
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
            form = super(projectstep_add, self).get_form(form_class)
            # form.fields['sdate'].widget.attrs['class'] = 'form-control datepicker'
            form.fields['edate'].widget.attrs['class'] = 'form-control datepicker'
            #form.fields['sdate'].input_formats=['%d-%m-%y', '%d-%m-%Y',]
            #form.fields['edate'].input_formats=['%d-%m-%y', '%d-%m-%Y',]
            form.fields['projectstep'].queryset=projectstep.objects.filter(project=self.p)
            return form
        return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.project = self.p
        instance.save()
        self.projectstep = instance
        return super(projectstep_add, self).form_valid(form)

#     #def get_context_data(self, *args, **kwargs):
#     #    context_data = super(projectstep_add, self).get_context_data(*args, **kwargs)
#     #    context_data.update({'object': self.data,})
#     #    return context_data

    def get_success_url(self): 
        #send telegram
        path_projectstep = reverse('project:projectstep_detail',args=[self.projectstep.id])
        today = datetime.date.today()
        value_user = u'Сегодня %s вы создали новый этап %s проекта %s (ссылка: crm.babah24.ru%s)' % (today, self.projectstep.name, self.p.name, path_projectstep)
        value_chat = u'Сегодня %s пользователь %s создал новый этап %s проекта %s (ссылка: crm.babah24.ru%s)' % (today, self.p.user, self.projectstep.name, self.p.name, path_projectstep)
         
        nh=notifyhandler.objects.get(name='telegram')

        try:
            nuk=notifyuserkey.objects.get(user=self.p.user, handler=nh)
        except:
            pass
        else: 
            nq=notifyqueue.objects.create(user=self.p.user, handler=nh, value=value_user)

        try:
             telegram_chat_user = User.objects.get(username='telegram_chat')
        except:
             pass
        else:
             nq=notifyqueue.objects.create(user=telegram_chat_user, handler=nh, value=value_chat)

        for e in self.projectstep.executor.all().exclude(user=self.p.user):
            value_executor = u' Сегодня %s вы стали исполнителем в новом этапе %s проекта %s (ссылка: crm.babah24.ru%s)' % (today, self.projectstep.name, self.p.name, path_projectstep)
            try:
                nuk=notifyuserkey.objects.get(user=e.user, handler=nh)
            except:
                pass
            else: 
                nq=notifyqueue.objects.create(user=e.user, handler=nh, value=value_executor)
        
        return reverse('project:project_detail',args=[self.p.id])

class projectstep_edit(UpdateView):
    model = projectstep
    template_name = '_edit2.html'
    fields = ['id', 'name', 'executor', 'distributor', 'edate', 'desc']

    def dispatch(self, request, *args, **kwargs):
        # self.data = get_object_or_404(projectstep, id=self.kwargs['pk'])
        return super(projectstep_edit, self).dispatch(request, *args, **kwargs)
    
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
            form = super(projectstep_edit, self).get_form(form_class)
            # form.fields['sdate'].widget.attrs['class'] = 'form-control datepicker'
            form.fields['edate'].widget.attrs['class'] = 'form-control datepicker'
            #form.fields['sdate'].input_formats=['%d-%m-%y', '%d-%m-%Y',]
            #form.fields['edate'].input_formats=['%d-%m-%y', '%d-%m-%Y',]
            return form
        return form_class(**self.get_form_kwargs())

    def get_object(self, queryset=None):
        self.data=super(projectstep_edit, self).get_object()
        if self.data.project.user != self.request.user:
            raise PermissionDenied
        return self.data

    def get_success_url(self):
        
        #send telegram
        today = datetime.date.today()
        path_projectstep = reverse('project:projectstep_detail',args=[self.data.id])
        value_user = u'Сегодня %s этап %s проекта %s был вами изменён (ссылка: crm.babah24.ru%s)' % (today, self.data.name, self.data.project.name, path_projectstep)
        value_chat = u'Сегодня %s пользователем %s этап %s проекта %s был изменён (ссылка: crm.babah24.ru%s)' % (today, self.data.project.user, self.data.name, self.data.project.name, path_projectstep)
         
        nh=notifyhandler.objects.get(name='telegram')

        try:
            nuk=notifyuserkey.objects.get(user=self.data.project.user, handler=nh)
        except:
            pass
        else: 
            nq=notifyqueue.objects.create(user=self.data.project.user, handler=nh, value=value_user)

        try:
             telegram_chat_user = User.objects.get(username='telegram_chat')
        except:
             pass
        else:
             nq=notifyqueue.objects.create(user=telegram_chat_user, handler=nh, value=value_chat)

        for e in self.data.executor.all().exclude(user=self.data.project.user):
            value_executor = u' Сегодня %s этап %s проекта %s, в котором вы участвуете, был изменён (ссылка: crm.babah24.ru%s)' % (today, self.data.name, self.data.project.name, path_projectstep)
            try:
                nuk=notifyuserkey.objects.get(user=e.user, handler=nh)
            except:
                pass
            else: 
                nq=notifyqueue.objects.create(user=e.user, handler=nh, value=value_executor)
      
        return path_projectstep

class projectstep_detail(CreateView): 
    template_name = 'projectstep_detail.html' 
    model = projectcomment
    fields = ['value']

    def dispatch(self, request, *args, **kwargs):
        self.data = get_object_or_404(projectstep, id=self.kwargs['pk'])
        return super(projectstep_detail, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        #instance.project = self.data.project
        instance.save()
        self.data.projectcomment.add(instance)

        #send telegram
        today = datetime.date.today()
        path_projectstep = reverse('project:projectstep_detail',args=[self.data.id])
        
        value_user = u'Сегодня %s пользователь %s оставил комментарий для этапа %s проекта %s (ссылка: crm.babah24.ru%s)' % (today, self.request.user, self.data.name, self.data.project.name, path_projectstep)
        value_chat = u'cСегодня %s пользователь %s оставил комментарий для этапа %s проекта %s (ссылка: crm.babah24.ru%s)' % (today, self.request.user, self.data.name, self.data.project.name, path_projectstep)

        nh=notifyhandler.objects.get(name='telegram')
        # send to user
        try:
            nuk=notifyuserkey.objects.get(user=self.data.project.user, handler=nh)
        except:
            pass
        else: 
            nq=notifyqueue.objects.create(user=self.data.project.user, handler=nh, value=value_user)
        # send to telegram_chat
        try:
             telegram_chat_user = User.objects.get(username='telegram_chat')
        except:
             pass
        else:
             nq=notifyqueue.objects.create(user=telegram_chat_user, handler=nh, value=value_chat)
        # send to executor
        for e in self.data.executor.all().exclude(user=self.data.project.user):
            value_executor = u'Сегодня %s пользователь %s оставил комментарий для этапа %s проекта %s, где вы участвуете  (ссылка: crm.babah24.ru%s)' % (today, self.request.user, self.data.name, self.data.project.name, path_projectstep)
            try:
                nuk=notifyuserkey.objects.get(user=e.user, handler=nh)
            except:
                pass
            else: 
                nq=notifyqueue.objects.create(user=e.user, handler=nh, value=value_executor)

        return super(projectstep_detail, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context_data = super(projectstep_detail, self).get_context_data(*args, **kwargs)
        context_data.update({'object': self.data,})
        return context_data

    def get_success_url(self):
        return reverse('project:projectstep_detail',args=[self.data.id])

class projectstep_success(UpdateView):
    model = projectstep
    template_name = '_edit2.html'
    fields = ['status']

    def dispatch(self, request, *args, **kwargs):
        # self.data = get_object_or_404(projectstep, id=self.kwargs['pk'])
        return super(projectstep_success, self).dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        self.data=super(projectstep_success, self).get_object()
        if self.data.project.user != self.request.user:
            raise PermissionDenied
        
        if self.data.projectstep is not None:
            if self.data.projectstep.status == True:
                raise Http404()
        return self.data

    def get_success_url(self):
        #send telegram
        today = datetime.date.today()
        path_projectstep = reverse('project:projectstep_detail',args=[self.data.id])
        
        value_user = u'Сегодня %s этап %s проекта %s был завершен(ссылка: crm.babah24.ru%s)' % (today, self.data.name, self.data.project.name, path_projectstep)
        value_chat = u'Сегодня %s этап %s проекта %s был завершен(ссылка: crm.babah24.ru%s)' % (today, self.data.name, self.data.project.name, path_projectstep)
        
        nh=notifyhandler.objects.get(name='telegram')
        # send to user
        try:
            nuk=notifyuserkey.objects.get(user=self.data.project.user, handler=nh)
        except:
            pass
        else: 
            nq=notifyqueue.objects.create(user=self.data.project.user, handler=nh, value=value_user)
        # send to telegram_chat
        try:
             telegram_chat_user = User.objects.get(username='telegram_chat')
        except:
             pass
        else:
             nq=notifyqueue.objects.create(user=telegram_chat_user, handler=nh, value=value_chat)
        # send to executor
        for e in self.data.executor.all().exclude(user=self.data.project.user):
            value_executor = u'Сегодня %s этап %s проекта %s, где вы участвуете, был завершен(ссылка: crm.babah24.ru%s)' % (today, self.data.name, self.data.project.name, path_projectstep)
            try:
                nuk=notifyuserkey.objects.get(user=e.user, handler=nh)
            except:
                pass
            else: 
                nq=notifyqueue.objects.create(user=e.user, handler=nh, value=value_executor)


        return path_projectstep


class projectstep_pict_add(CreateView): 
    template_name = 'project_file_add.html'
    fields = ['pict', 'desc']
    model = projectpict

    def dispatch(self, request, *args, **kwargs):
        self.data = get_object_or_404(projectstep, id=self.kwargs['pk'], project__user=self.request.user)
        return super(projectstep_pict_add, self).dispatch(request, *args, **kwargs)
        
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        # instance.project = self.data
        instance.save()
        self.data.pict.add(instance)
        return super(projectstep_pict_add, self).form_valid(form)

    def get_success_url(self):
        return reverse('project:projectstep_detail',args=[self.data.id])

class projectstep_pict_del(DeleteView): 
    template_name = '_confirm_delete.html' 
    model = projectpict

    def dispatch(self, request, *args, **kwargs):
        return super(projectstep_pict_del, self).dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        self.data=super(projectstep_pict_del, self).get_object()
        if self.data.projectstep_set.first().project.user != self.request.user:
            raise PermissionDenied
        return self.data

    def get_context_data(self, **kwargs):
        context = super(projectstep_pict_del, self).get_context_data(**kwargs)
        context['msg'] = u'Вы уверены что хотите удалить '
        context['back_url'] = reverse('project:projectstep_detail',args=[self.data.projectstep_set.all().first().project.id])
        return context

    def get_success_url(self):
        return reverse('project:projectstep_detail',args=[self.data.projectstep_set.all().first().project.id])

class projectstep_file_add(CreateView): 
    template_name = 'project_file_add.html'
    fields = ['sourcefile', 'desc']
    model = projectfile

    def dispatch(self, request, *args, **kwargs):
        self.data = get_object_or_404(projectstep, id=self.kwargs['pk'], project__user=self.request.user)
        return super(projectstep_file_add, self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        # instance.project = self.data
        instance.save()
        self.data.file.add(instance)
        return super(projectstep_file_add, self).form_valid(form)

    def get_success_url(self):
        return reverse('project:projectstep_detail',args=[self.data.id])

class projectstep_file_del(DeleteView): 
    template_name = '_confirm_delete.html'
    model = projectfile

    def dispatch(self, request, *args, **kwargs):
        return super(projectstep_file_del, self).dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        self.data=super(projectstep_file_del, self).get_object()
        if self.data.projectstep_set.first().project.user != self.request.user:
            raise PermissionDenied
        return self.data
    
    def get_context_data(self, **kwargs):
        context = super(projectstep_file_del, self).get_context_data(**kwargs)
        context['msg'] = u'Вы уверены что хотите удалить '
        context['back_url'] = reverse('project:projectstep_detail',args=[self.data.projectstep_set.all().first().id])
        return context

    def get_success_url(self):
        return reverse('project:projectstep_detail',args=[self.data.projectstep_set.all().first().id])

class projectstepcomment_edit(UpdateView):
    model = projectcomment
    template_name = '_edit2.html'
    fields = ['value']

    def dispatch(self, request, *args, **kwargs):
        return super(projectstepcomment_edit, self).dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        self.data=super(projectstepcomment_edit, self).get_object()
        if self.data.user != self.request.user:
            raise PermissionDenied
        return self.data

    def get_success_url(self):
        return reverse('project:projectstep_detail',args=[self.data.projectstep_set.all().first().id])

class projectstepcomment_del(DeleteView): 
    template_name = '_confirm_delete.html' 
    model = projectcomment

    def dispatch(self, request, *args, **kwargs):
        return super(projectstepcomment_del, self).dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        self.data=super(projectstepcomment_del, self).get_object()
        if self.data.user != self.request.user:
            raise PermissionDenied
        return self.data

    def get_context_data(self, **kwargs):
        context = super(projectstepcomment_del, self).get_context_data(**kwargs)
        context['msg'] = u'Вы уверены что хотите удалить '
        context['back_url'] = reverse('project:projectstep_detail',args=[self.data.projectstep_set.all().first().id])
        return context

    def get_success_url(self):
        return reverse('project:projectstep_detail',args=[self.data.projectstep_set.all().first().id])

class projectstepcomment_pict_add(CreateView):
    model = projectpict
    template_name = 'project_file_add.html'
    fields = ['pict', 'desc']
#     #success_url = '/project/list/'

    def dispatch(self, request, *args, **kwargs):
        self.comment = get_object_or_404(projectcomment, id=self.kwargs['pk'], user=request.user)
        return super(projectstepcomment_pict_add, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.projectcomment = self.comment
        instance.save()
        self.comment.pict.add(instance)
        return super(projectstepcomment_pict_add, self).form_valid(form)

    def get_success_url(self):
        return reverse('project:projectstep_detail',args=[self.comment.projectstep_set.all().first().id])

class projectstepcomment_pict_del(DeleteView):
    model = projectpict
    template_name = '_confirm_delete.html'
    
    def dispatch(self, request, *args, **kwargs):
        return super(projectstepcomment_pict_del, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        self.data=super(projectstepcomment_pict_del, self).get_object()
        if self.data.projectcomment_set.all().first().user != self.request.user:
            raise PermissionDenied
        return self.data
    
    def get_context_data(self, **kwargs):
        context = super(projectstepcomment_pict_del, self).get_context_data(**kwargs)
        context['msg'] = u'Вы уверены что хотите удалить '
        context['back_url'] = reverse('project:projectstep_detail',args=[self.data.projectcomment_set.all().first().projectstep_set.all().first().id])
        return context

    def get_success_url(self):
        return reverse('project:projectstep_detail',args=[self.data.projectcomment_set.all().first().projectstep_set.all().first().id])

class projectstepcomment_file_add(CreateView): 
    template_name = 'project_file_add.html' 
    model = projectfile
    fields = ['sourcefile', 'desc']

    def dispatch(self, request, *args, **kwargs):
        self.comment = get_object_or_404(projectcomment, id=self.kwargs['pk'], user=request.user)
        return super(projectstepcomment_file_add, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.projectcomment = self.comment
        instance.save()
        self.comment.file.add(instance)
        return super(projectstepcomment_file_add, self).form_valid(form)

    def get_success_url(self):
        return reverse('project:projectstep_detail',args=[self.comment.projectstep_set.all().first().id])

class projectstepcomment_file_del(DeleteView): 
    template_name = '_confirm_delete.html' 
    model = projectfile

    def dispatch(self, request, *args, **kwargs):
        return super(projectstepcomment_file_del, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        self.data=super(projectstepcomment_file_del, self).get_object()
        if self.data.projectcomment_set.all().first().user != self.request.user:
            raise PermissionDenied
        return self.data
    
    def get_context_data(self, **kwargs):
        context = super(projectstepcomment_file_del, self).get_context_data(**kwargs)
        context['msg'] = u'Вы уверены что хотите удалить '
        context['back_url'] = reverse('project:projectstep_detail',args=[self.data.projectcomment_set.all().first().projectstep_set.all().first().id])
        return context

    def get_success_url(self):
        return reverse('project:projectstep_detail',args=[self.data.projectcomment_set.all().first().projectstep_set.all().first().id])


class projectstep_cost_add(CreateView): 
    template_name = '_edit2.html'
    fields = ['typecost', 'name', 'distributor', 'costsum']
    model = projectstepcost

    def dispatch(self, request, *args, **kwargs):
        self.data = get_object_or_404(projectstep, id=self.kwargs['pk'])
        return super(projectstep_cost_add, self).dispatch(request, *args, **kwargs)
    
    def get_form(self, form_class=None):

        if self.data.project.user != self.request.user and self.request.user not in [e.user for e in self.data.executor.all()]:
            raise PermissionDenied

        if form_class is None:
            form_class = self.get_form_class()
            form = super(projectstep_cost_add, self).get_form(form_class)
            form.fields['distributor'].queryset=distributor.objects.filter(projectstep=self.data)
            form.fields['typecost'].initial='plan'
            if self.data.project.user !=self.request.user:
                form.fields['typecost'].initial='fact'
                form.fields['typecost'].widget.attrs['disabled'] = True
                form.fields['typecost'].required=False
            return form
        return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        self.data.cost.add(instance)
        return super(projectstep_cost_add, self).form_valid(form)

    def get_success_url(self):
        return reverse('project:projectstep_detail',args=[self.data.id])

