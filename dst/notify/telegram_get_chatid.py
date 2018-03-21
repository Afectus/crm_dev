#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, django

projecthome = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if projecthome not in sys.path:
    sys.path.append(projecthome)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj.settings")
django.setup()


import time
import requests
import datetime
from django.utils import timezone

from notify.models import *
from dj.views import *
from notify.views import *

import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters

token = '423858151:AAHBOinWfJB97khDwLIuUA8DZitomI7bELU'

bot = telegram.Bot(token=token)

print(bot.get_me()) #info bot

bot.send_message(chat_id='-287576538', text='chatid bot start')


#get chat id
updater = Updater(token=token)
dispatcher = updater.dispatcher

def get_chat_id(bot, update):
	#print(bot)
	#print(update)
	print(update.message.chat_id)
	bot.send_message(chat_id=update.message.chat_id, text='chat id=%s' % (update.message.chat_id))

echo_handler = MessageHandler(Filters.all, get_chat_id)
dispatcher.add_handler(echo_handler)

updater.start_polling()

