from .models import *
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from acl.views import get_object_or_denied
# Менеджмент вьюхи

class list_points_managment(ListView):
    model = points
    template_name = 'list_points_managment.html'
    paginate_by = 30


    def dispatch(self, request, *args, **kwargs):
        get_object_or_denied(self.request.user, 'list_points_managment', 'L') #проверяем права
        return super(list_points_managment, self).dispatch(request, *args, **kwargs)


class show_points_managment(DetailView):
    model = points
    template_name = 'show_points_managment.html'

    def dispatch(self, request, *args, **kwargs):
        get_object_or_denied(self.request.user, 'list_points_managment', 'L') #проверяем права
        return super(show_points_managment, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_show_points_managment = points.objects.get(id=self.kwargs['pk'])
        context_data = super(show_points_managment, self).get_context_data(**kwargs)
        context_data.update({'context_show_points_managment': context_show_points_managment})
        return context_data


class create_points_managment(CreateView):
    model = points
    template_name = 'create_points_managment.html'
    fields = ['user', 'type', 'point','comment']


    def dispatch(self, request, *args, **kwargs):
        get_object_or_denied(self.request.user, 'create_points_managment', 'L') #проверяем права
        return super(create_points_managment, self).dispatch(request, *args, **kwargs)



    def get_success_url(self):
        return reverse_lazy('list_points_managment')
    

class delete_points_managment(DeleteView):
    model = points
    template_name = 'delete_points_managment.html'


    def dispatch(self, request, *args, **kwargs):
        get_object_or_denied(self.request.user, 'delete_points_managment', 'L') #проверяем права
        return super(delete_points_managment, self).dispatch(request, *args, **kwargs)


    def get_success_url(self):
        return reverse_lazy('list_points_managment')
        


class update_points_managment(UpdateView):
    model = points
    template_name = 'update_points_managment.html'
    fields = ['user', 'type', 'point','comment']


    def dispatch(self, request, *args, **kwargs):
        get_object_or_denied(self.request.user, 'update_points_managment', 'L') #проверяем права
        return super(update_points_managment, self).dispatch(request, *args, **kwargs)


    def get_success_url(self):
        return reverse_lazy('list_points_managment')