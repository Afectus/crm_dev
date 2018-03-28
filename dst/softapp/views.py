from .models import *
from django.views.generic import ListView, DetailView
from acl.views import get_object_or_denied
from django.http import HttpResponse
import os
from django.conf import settings
from django.http import HttpResponse

class softs_list(ListView):
    """Вьюшка для просмотра списка новостей"""
    model = softs
    template_name = 'softs_list.html'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        #get_object_or_denied(self.request.user, 'softapp', 'L') #проверяем права
        return super(softs_list, self).dispatch(request, *args, **kwargs)



class softs_detail(DetailView):
    model = softs
    template_name = 'softs_detail.html'

    def dispatch(self, request, *args, **kwargs):
        #get_object_or_denied(self.request.user, 'softapp', 'L') #проверяем права
        return super(softs_detail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_show_softs = softs.objects.get(id=self.kwargs['pk'])
        context_data = super(softs_detail, self).get_context_data(**kwargs)
        context_data.update({'context_show_softs': context_show_softs})
        return context_data
