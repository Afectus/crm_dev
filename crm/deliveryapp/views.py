from .models import *
from notify.models import *
from telegramtemplate.models import *

from django.views.generic.edit import CreateView, DeleteView, UpdateView ,FormView
from django.views.generic import ListView,DetailView
from django.urls import reverse_lazy,reverse
from django.shortcuts import get_object_or_404
from acl.views import get_object_or_denied
from django.shortcuts import HttpResponseRedirect
from django import forms

def get_message(typetemplate, user, path):
    # Переменные шаблона:<br>
    # (today) - Сегодняшняя дата<br>
    # (user) - Пользователь<br>
    # (url) - Ссылка на объект (crm.babah24.ru)<br>
    #today = datetime.date.today()
    now = datetime.datetime.now()

    fullname = user.first_name + " " + user.last_name

    t = telegramtemplate.objects.filter(name=typetemplate)
    t = t.first()
    message = t.message
    message = message.replace('(today)', now.strftime('%d-%m-%Y %H:%M:%S'))
    message = message.replace('(user)', str(fullname))
    message = message.replace('(url)', 'crm.babah24.ru%s' % path)
    return message

# отправляем сообщения в очередь
def send_message(iuser, message):
    nh=notifyhandler.objects.get(name='telegram_chat')
    nq=notifyqueue.objects.create(handler=nh, value=message)


class Form_filter_order(forms.Form):

	sortchoice=(
		('ctime', 'Старые'),
		('-ctime', 'Новые'),
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

        if 'mydelivery' not in self.request.session:
            self.request.session['mydelivery'] = ''

        if self.request.GET.get('mydelivery'):
            self.request.session['mydelivery'] = 'True'
        elif self.request.GET.get('alldelivery'):
            self.request.session['mydelivery'] = 'False'

        return data

    def get_context_data(self, *args, **kwargs):
        context_data = super(dellist_list, self).get_context_data(*args, **kwargs)
        context_data.update({'form': Form_filter_order(self.request.GET),})
        return context_data

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
        comments = "%s создал доставку id: %s"%(self.request.user, instance.id)
        de=delevent.objects.create(user=self.request.user, dellist=instance, event='add', comment=comments,)

        path = reverse('dellist_detail', args=[instance.id])
        value_chat = get_message('dellist_add', self.request.user, path)
        send_message(User.objects.get(username='telegram_chat'), value_chat)

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
        comments = "%s отредактировал доставку id: %s"%(self.request.user, instance.id)
        de=delevent.objects.create(user=self.request.user, dellist=instance, event='edit', comment=comments,)

        path = reverse('dellist_detail', args=[instance.id])
        value_chat = get_message('dellist_edit', self.request.user, path)
        send_message(User.objects.get(username='telegram_chat'), value_chat)

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

    path = reverse('dellist_detail', args=[data.id])
    value_chat = get_message('dellist_accept', request.user, path)
    send_message(User.objects.get(username='telegram_chat'), value_chat)

    return HttpResponseRedirect(reverse('dellist_detail', args=[data.id]))

def dellist_success(request, pk):
    data = get_object_or_404(dellist, id=pk, status='accept')
    #get_object_or_denied(request.user, 'deliveryapp', 'C')
    data.status='success'
    data.save()
    comments = "%s выполнил доставку id: %s"%(request.user, data.id)

    path = reverse('dellist_detail', args=[data.id])
    value_chat = get_message('dellist_success', request.user, path)
    send_message(User.objects.get(username='telegram_chat'), value_chat)

    de=delevent.objects.create(user=request.user, dellist=data, event='success', comment=comments,)
    return HttpResponseRedirect(reverse('dellist_detail', args=[data.id]))
