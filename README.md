## ПОРЯДОК ОФОРМЛЕНИЕ КОДА

#### НАСТРОЙКИ ПРОЕКТА dj

основные настройки храним в ```settings.py```, личные настройки проекта храним в ```settings_local.py``` который не будет выгружаться в репозиторий

пример использования settings.py:
```python
# глобальное подключение к базе данных
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'shop',
		'USER': 'shop',
		'PASSWORD': 'shop',
		'HOST': '127.0.0.1',
		'PORT': '5432',
	}
}

# в конце файла settings.py подключаем кастомные настройки settings_local.py
try:
	from dj.settings_local import *
except:
	pass
```

кастомные настройки: settings_local.py

```python
# ваше текущее подключение к базе данных
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'shop',
		'USER': 'shop',
		'PASSWORD': 'shop',
		'HOST': '192.168.0.33',
		'PORT': '5433',
	}
}
```



#### ПРИЛОЖЕНИЕ app

шаблон имени: **xxxxapp**

```python
# пример
INSTALLED_APPS = [
	'shopapp',
	'banerapp',
	'newsapp',
	...
]
urlpatterns = [
	url(r'^', include('shopapp.urls')),
	url(r'^', include('banerapp.urls')),
	url(r'^', include('newsapp.urls')),
	...
```

***

#### МОДЕЛЬ models.py

шаблон имени: **xxxxitem**, **xxxxlist**, **xxxxs**


использование доп. атрибутов для полей модели
```python
# по умолчанию модель должна отвечать за обязательность заполнения полей
myfield = models.CharField(verbose_name='myfield', max_length=200)
# или
myfield = models.CharField(verbose_name='myfield', max_length=200, blank=False, null=False)
#
# если архитектурой проекта предусмотрены необязательные поля
myfield = models.CharField(verbose_name='myfield', max_length=200, blank=True, null=False)
#
# необязательные поля для типа ForeignKey()
user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
```

загрузка картинок в модель при помощи функции **make_upload_path** или **make_upload_file** из **dj.views**

```python
# пример
from dj.views import *

class newslist(models.Model): #newslist, newss
	id = models.AutoField(primary_key=True, unique=True) #обязательное поле
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(verbose_name='Название', max_length=200)
	pict = models.ImageField(upload_to=make_upload_file, verbose_name='Изображение')
	pict40 = ImageSpecField(source='pict', processors=[ResizeToFit(40, 40)], format='PNG', options={'quality': 95})
	pict100 = ImageSpecField(source='pict', processors=[ResizeToFit(100, 100)], format='PNG', options={'quality': 95})

	def __str__(self):
		return u'%s' % (self.id, self.name)
```

все связи моделей по возможности делаем через models.ForeignKey()
```python
# пимер связи таблицы mytest и User по полю user
# плюсы подхода, автоматические удаление связанных полей
class test(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	
```

```python
# использование связи MTM рекомендуется использовать в крайних случаях
# минусы подхода, ручное удаление связанных полей
class mytest(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	user = models.ManyToManyField(User)
	value = models.TextField(verbose_name='Комментарии')
	pict = models.ManyToManyField(projectpict, blank=True)
	
```

названия моделей обозначаем нижним регистром, игнорируем рекомендации Django
```python
class mytest(models.Model): #+
class Mytest(models.Model): #-
```

рекомендуемые поля при создании модели
```python
class mytest(models.Model):
	ctime = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
	# ctime выполняет функцию отслеживания даты создания объекта
	utime = models.DateTimeField(verbose_name='Дата обновления объекта', auto_now=True)
	# utime выполняет функцию отслеживания даты последнего обновления объекта
	# так же может быть обновлена принудительно, пример object.utime = datetime.datetime.now()
	#
	name = models.CharField(verbose_name='Название', max_length=100)
	# если нет возможности использоват name, например при конфликте с встроенными функциями, то используем
	title = models.CharField(verbose_name='Заголовок', max_length=100)
	#
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	#user определяет принадлежность объекта к пользователю, доп. атрибуты null=True, blank=True
	#
	# seo оптимизация (для публичной части интернет страниц)
	seo_title = models.CharField(max_length=255, blank=True)
	seo_description = models.CharField(max_length=255, blank=True)
	seo_keywords = models.CharField(max_length=255, blank=True)
```

***

#### УПРАВЛЕНИЕ ЭЛЕМЕНТАМИ admin.py

```python
# пример
from .models import *

class newslistAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'name', 'pict',)
admin.site.register(newslist, newslistAdmin)
```

***

#### УПРАВЛЕНИЕ ЭЛЕМЕНТАМИ panel.py

шаблон имени класса

- список элементов: '''python panel_названиемодели_list(ListView)'''
- добавление элемента: '''python panel_названиемодели_add(CreateView)'''
- удаление элемента: panel_'''python названиемодел_del(DeleteView)'''
- редактирование элемента: '''python panel_названиемодел_edit(UpdateView)'''


```python
# пример
from acl.views import get_object_or_denied
# (('A', 'All'), ('L', 'Список'), ('R', 'Чтение'), ('C', 'Создание'), ('U', 'Редактирование'),)

class panel_newslist_list(ListView):
	model = newslist
	template_name = 'panel_newslist_list.html'
	# для вывода списка элементов в шаблоне использовать переменную object_list

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'newslist', 'L') # проверяем права
		return super(panel_newslist_list, self).dispatch(request, *args, **kwargs)
		
		
class panel_newslist_add(CreateView):
	model = newslist
	template_name = 'panel_newslist_add.html'
	fields = ['name', 'pict']

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'newslist', 'C') # проверяем права
		return super(panel_newslist_add, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		instance.save()
		self.data = instance
		return super(panel_newslist_add, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('panel_newslist_list')
		

class panel_newslist_del(DeleteView):
	model = newslist
	template_name = 'panel_newslist_del.html'

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'baner', 'U') # проверяем права
		return super(panel_newslist_del, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return reverse_lazy('panel_newslist_list')
		
		
class panel_newslist_edit(UpdateView):
	model = newslist
	template_name = 'panel_newslist_edit.html'
	fields = ['url', 'pict']

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'baner', 'U') # проверяем права
		return super(panel_newslist_edit, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		instance.save()
		self.data = instance
		return super(panel_newslist_edit, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('panel_newslist_list')
		
```

***

#### РОУТИНГ url.py

- url типа **'/panel/newslist/list/'** передает управление классу **panel_newslist_list** (```/``` замена на ```_```)

- каноническое имя url идентично названию класса **panel_newslist_list**

- при обращении к url через ```reverse_lazy('panel_newslist_list')``` понимаем, что будет вызван ```class panel_newslist_list(ListView):``` из **panel.py** приложения

- завершающий символ ```?``` обязателен для url ```'^/newslist/list/?$'```, так как позволяет пользователям открывать страницу по адресам **/newslist/list/** и **/newslist/list**

```python
# пример
from django.contrib.auth.decorators import login_required

from .views import *
from .panel import *

urlpatterns = [
	# views.py публичная часть
	re_path('^/newslist/list/?$', newslist_list.as_view(), name='newslist_list'),
	# panel.py приватная часть
	re_path('^/panel/newslist/list/?$', login_required(panel_newslist_list.as_view()), name='panel_newslist_list'),
	re_path('^/panel/newslist/add/?$', login_required(panel_newslist_add.as_view()), name='panel_newslist_add'),
	re_path('^/panel/newslist/del/(?P<pk>\d+)/?$', login_required(panel_newslist_del.as_view()), name='panel_newslist_del'),
	re_path('^/panel/newslist/edit/(?P<pk>\d+)/?$', login_required(panel_newslist_edit.as_view()), name='panel_newslist_edit'),
]
```

***

#### ШАБЛОНЫ templates

шаблоны приложений храняться в каталоге **newsapp/templates**

публичная часть
- шаблон наследования: **template/base.html**
- список элементов: **newsapp/templates/newslist_list.html**

приватная часть
- шаблон наследования: **template/panel_base.html**
- список элементов: **newsapp/templates/panel_newslist_list.html**
- добавление элемента: **newsapp/templates/panel_newslist_add.html**
- удаление элемента: **newsapp/templates/panel_newslist_del.html**
- редактирование элемента: **newsapp/templates/panel_newslist_edit.html**

```html
<!-- пример базового шаблона приватной части -->
{% extends "panel_base.html" %}
{% block title %}Панель управления{% endblock %}
{% block description %}Панель управления{% endblock %}
{% block keywords %}{% endblock %}

{% block content %}

{% load nodetag %}

{% load newsapptag %} <!-- если необходимо подключаем кастомные теги -->

{% include "paginator.html" %} <!-- если необходимо подключаем пагинатор -->

{% endblock %}

```

```html
<!-- пример базового шаблона публичной части элемента детально -->
{% extends "base.html" %}
{% block title %} {{ object.seo_title }} {% endblock %}
{% block description %} {{ object.seo_description }} {% endblock %}
{% block keywords %} {{ object.seo_keywords }} {% endblock %}

{% block content %}

{% load nodetag %}

{% load newsapptag %} <!-- если необходимо подключаем кастомные теги -->

<h1>{{ object.name }}</h1>

{% endblock %}
```

```html
<!-- пример базового шаблона публичной части списка элементов -->
{% extends "base.html" %}
{% block title %}{% endblock %}
{% block description %}{% endblock %}
{% block keywords %}{% endblock %}

{% block content %}

{% load nodetag %}

{% load newsapptag %} <!-- если необходимо подключаем кастомные теги -->

{% for i in object_list %} <!-- забираем данные из встроенной переменной object_list -->
	{{ i.name }}
{% endfor %}

{% include "paginator.html" %} <!-- если необходимо подключаем пагинатор -->

{% endblock %}
```

комментирование участков кода в шаблоне средствами шаблонизатора Django 
```
{% comment %}
<div class="test">test</div>
{% endcomment %}
```
	
плохой пример комментирования, отнимает ресурсы
```
<!-- 
<div class="test">test</div>
-->
```





***

#### КАСТОМЫНЕ ТЭГИ templatetags
кастомыне теги храняться в  **newsapp/templatetags/newsapptag.py**


***
### РЕЦЕПТЫ

счетчик просмотров ```pip install django-hitcount```
```python
# in models.py
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin
from hitcount.models import HitCount

class newss(models.Model, HitCountMixin):
	hitcount = GenericRelation(HitCount, object_id_field='id', related_query_name='hit_count_generic_relation',)

# in views.py
from hitcount.views import HitCountDetailView

class newss_detail(HitCountDetailView): # класс HitCountDetailView наследует класс DetailView
	model = newss
	template_name = 'newss_detail.html'
	count_hit = True

# in template
{% for newsitem in object_list %}
	newsitem.hit_count.hits
{% endfor %}
```



