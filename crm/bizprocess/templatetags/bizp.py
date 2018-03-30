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

register = template.Library()

from node.models import *
from bizprocess.models import *



@register.simple_tag
def getsteplevel2list(id):
	#from node.models import propertiesvalue
	return bizpstep.objects.filter(parent=id).order_by('sort')
	
	

