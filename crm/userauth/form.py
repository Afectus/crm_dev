# -*- coding: utf-8 -*-
from django import forms
import re
import os
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from django.utils.safestring import mark_safe

from django.core.exceptions import ObjectDoesNotExist


from captcha.fields import CaptchaField

from node.models import *

from .models import *



class Form_login(forms.Form):
	username = forms.CharField(widget=forms.TextInput({'class': 'form-control', 'placeholder': u'Логин'}), label=u'Логин', max_length=100, required=True)
	password = forms.CharField(widget=forms.PasswordInput({'class': 'form-control', 'placeholder': u'Пароль'}), label=u'Пароль', max_length=100, required=True)
	next = forms.CharField(widget=forms.HiddenInput(), max_length=100, required=True)

