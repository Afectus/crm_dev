from .models import *
from django.views.generic.edit import CreateView, DeleteView, UpdateView ,FormView
from django.views.generic import ListView,DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from acl.views import get_object_or_denied
#(('A', 'All'), ('L', 'Список'), ('R', 'Чтение'), ('C', 'Создание'), ('U', 'Редактирование'),)


# Менеджмент вьюхи

class panel_softs_list(ListView):
    model = softs
    template_name = 'panel_softs_list.html'


    def dispatch(self, request, *args, **kwargs):
        get_object_or_denied(self.request.user, 'softapp', 'L') #проверяем права
        return super(panel_softs_list, self).dispatch(request, *args, **kwargs)

class panel_softs_add(CreateView):
    model = softs
    template_name = 'panel_softs_add.html'
    fields = ['name', 'desc', 'soft',]


    def dispatch(self, request, *args, **kwargs):
        get_object_or_denied(self.request.user, 'softapp', 'C') #проверяем права
        return super(panel_softs_add, self).dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.createuser = self.request.user
        instance.updateuser = self.request.user
        instance.save()
        self.data = instance
        return super(panel_softs_add, self).form_valid(form)


    def get_success_url(self):
        return reverse_lazy('panel_softs_list')
    

class panel_softs_del(DeleteView):
    model = softs
    template_name = 'panel_softs_del.html'


    def dispatch(self, request, *args, **kwargs):
        get_object_or_denied(self.request.user, 'softapp', 'U') #проверяем права
        return super(panel_softs_del, self).dispatch(request, *args, **kwargs)


    def get_success_url(self):
        return reverse_lazy('panel_softs_list')
        


class panel_softs_edit(UpdateView):
    model = softs
    template_name = 'panel_softs_edit.html'
    fields = ['name', 'desc', 'soft',]


    def dispatch(self, request, *args, **kwargs):
        get_object_or_denied(self.request.user, 'softapp', 'U') #проверяем права
        return super(panel_softs_edit, self).dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.updateuser = self.request.user
        instance.save()
        self.data = instance
        return super(panel_softs_edit, self).form_valid(form)


    def get_success_url(self):
        return reverse_lazy('panel_softs_list')
