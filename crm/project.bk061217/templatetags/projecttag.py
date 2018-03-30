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

@register.assignment_tag
def projectstep_plansum(obj):
	obj = obj.filter(typecost='plan')
	return obj

@register.assignment_tag
def projectstep_factsum(obj):
	obj = obj.filter(typecost='fact')
	return obj

@register.assignment_tag
def projectstep_executors(obj):
	euserlist = [e.user for e in obj.executor.all()]
	return euserlist
