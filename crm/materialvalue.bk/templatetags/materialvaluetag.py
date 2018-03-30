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


from materialvalue.models import *

@register.simple_tag
def previous_location(materialvaluemove):
	mv = materialvalue.objects.filter(materialvaluemove=materialvaluemove).first()
	res = mv.materialvaluemove_set.all().filter(id__lt=materialvaluemove.id).last()
	return res
