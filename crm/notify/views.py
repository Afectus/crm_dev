# -*- coding: utf-8 -*- 
from __future__ import unicode_literals

from django.shortcuts import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponsePermanentRedirect

from django.core.exceptions import PermissionDenied

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django import forms
from django.contrib.auth.models import User, Group

import json
from django.core import serializers

from django.http import QueryDict

from django.views.generic import DetailView, ListView, DeleteView
from django.views.generic.edit import FormView, UpdateView
from django.views.generic.base import TemplateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator

from django.urls import reverse

import datetime, time

from django.db.models import Sum, Count, Q, IntegerField
from django.db.models.functions import Cast

from django.views.decorators.csrf import csrf_exempt

import urllib
import re
import requests

from django.conf import settings

from django.utils.encoding import force_text

from .models import *
from notify.models import *

from django.core.mail import send_mail


import logging
log = logging.getLogger(__name__)



# #
import telegram
from telegram.ext import Updater
# #


def telegram_bot_notify(chatid, value):
	token = settings.TELEGRAM_BOT_NOTIFY_TOKEN
	bot = telegram.Bot(token=token)
	res = bot.send_message(chat_id=chatid, text=value)
	return res

def telegram_bot_chat(chatid, value):
	token = settings.TELEGRAM_BOT_CHAT_TOKEN
	bot = telegram.Bot(token=token)
	res = bot.send_message(chat_id=chatid, text=value)
	return res

# def notifysend(user, value, chat=True, type='telegram'):
	# res = False
	# if type=='telegram':
		# try:
			# nh=notifyhandler.objects.get(name='telegram')
		# except:
			# pass
		# else:
			
		# return False
		# today = datetime.date.today()
		# telegram_chat_user = User.objects.get(username='telegram_chat')
	
	# return res
	
	
	