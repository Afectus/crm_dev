# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response



from django.db.models import Sum, Q, F, Count, TextField
from django.db.models.functions import Cast

from django.utils.safestring import mark_safe
from django.utils.numberformat import format

from django.contrib.auth.models import User, Group, UserManager

import re, datetime

from django import template

register = template.Library()


from project.models import *

@register.simple_tag
def projectstep_plansum(obj):
	obj = obj.filter(typecost='plan')
	return obj

@register.simple_tag
def projectstep_factsum(obj):
	obj = obj.filter(typecost='fact')
	return obj

@register.simple_tag
def projectstep_executors(obj):
	euserlist = [e.user for e in obj.executor.all()]
	return euserlist

@register.simple_tag
def project_completion_percents(obj):
	project_steps = obj.projectstep_set.all()
	steps_number = project_steps.count()
	counter = 0
	percents = 0
	if not project_steps:
		return percents
	else:
		for ps in project_steps:
			if not ps.status:
				counter = counter + 1
		percents = counter * 100 / steps_number 
	return percents
