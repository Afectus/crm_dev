# -*- coding: utf-8 -*-
from django import forms
import re
import os
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from captcha.fields import CaptchaField

from django.utils.safestring import mark_safe

from django.core.exceptions import ObjectDoesNotExist


def validate_phone(value):
	p = re.compile('^9[0-9]{9}$')
	if not p.match(value):
		raise ValidationError(u'формат телефона должен быть например +79025112233. ')
	
	
class Form_order(forms.Form):
	uname = forms.CharField(label='Ваше имя', help_text='Укажите Ваше имя', widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=50, required=True)
	
	phone = forms.CharField(label='Мобильный телефон', help_text='Укажите мобильный телефон', widget=forms.TextInput(attrs={'class': 'form-control',}), max_length=10, required=False, validators=[validate_phone])

	city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',}), label="Город", max_length=100, required=False)
	
	addr = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',}), label="Город", max_length=300, required=False)

	

