# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response


from django.db.models import Sum, Q, F, Count

from django.utils.safestring import mark_safe
from django.utils.numberformat import format

from django.contrib.auth.models import User, Group, UserManager

import re

from django import template
from panel.models import profileuser

register = template.Library()
from operator import itemgetter

@register.simple_tag
def amount_estimates(obj):
	# print(obj)
	a = obj.filter(value=5).count()
	b = obj.filter(value=4).count()
	c = obj.filter(value=3).count()
	d = obj.filter(value=2).count()
	e = obj.filter(value=1).count()
	return [a,b,c,d,e]

#### возвращаем топ по бирже идей
@register.simple_tag
def thebestofthebest():
	users = profileuser.objects.all()
	#top_generators
	count_ideas = {}
	count_likes = {}
	count_adopted = {}
	for u in users:
		count_ideas.update({u: u.useridea_set.all().count()})
		count_likes.update({u: u.likeidea_set.all().count()})
		count_adopted.update({u: u.useridea_set.filter(status='adopted').count()})

	# определяем топ
	count_ideas_max_number = max(count_ideas.items(), key=itemgetter(1))[1]
	count_likes_max_number= max(count_likes.items(), key=itemgetter(1))[1]
	count_adopted_max_number = max(count_adopted.items(), key=itemgetter(1))[1]

	count_ideas = {d for d in count_ideas.items() if d[1] == count_ideas_max_number}
	count_likes = {d for d in count_likes.items() if d[1] == count_likes_max_number}
	count_adopted = {d for d in count_adopted.items() if d[1] == count_adopted_max_number}
	
	return [count_ideas, count_likes, count_adopted]

### отчет по активности пользователей в бирже идей
def report_profileusers_activity():
	users = profileuser.objects.all()
	#top_generators
	count_ideas = {}
	count_likes = {}
	count_adopted = {}
	for u in users:
		count_ideas.update({u: u.useridea_set.all().count()})
		count_likes.update({u: u.likeidea_set.all().count()})
		count_adopted.update({u: u.useridea_set.filter(status='adopted').count()})

	count_ideas = sorted(count_ideas.items(), key=itemgetter(1), reverse=True)
	count_likes = sorted(count_likes.items(), key=itemgetter(1), reverse=True)
	count_adopted = sorted(count_adopted.items(), key=itemgetter(1), reverse=True)

	# print(count_ideas)
	# print(count_likes)
	# print(count_adopted)

	return [count_ideas, count_likes, count_adopted]
