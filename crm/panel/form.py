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

from panel.models import *



def validate_phone8(value):
	p = re.compile('^89[0-9]{9}$')
	if not p.match(value):
		raise ValidationError(u'формат телефона должен быть например 89025112233. ')
		
		
class Form_sms(forms.Form):
	phone = forms.CharField(label='Номер телефона', help_text='Укажите номер телефона', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'on'}), max_length=11, required=True, validators=[validate_phone8])

	message = forms.CharField(widget=forms.Textarea(attrs={'cols': '40', 'rows': '10',}), label=u'Сообщение', max_length=300, required=True)
	
	
class Form_sms2b(forms.Form):
	message = forms.CharField(widget=forms.Textarea(attrs={'cols': '40', 'rows': '10',}), label=u'Сообщение', max_length=300, required=True)

	
def validate_phone_isuse(value):
	p = re.compile('^9[0-9]{9}$')
	if not p.match(value):
		raise ValidationError(u'формат телефона должен быть например 9025112233. ')
	try:
		p=profileuser.objects.get(phone=value)
	except:
		raise ValidationError(u'Номер %s не зарегистрирован. ' % value)

		
	
class Form_user_restore(forms.Form):
	phone = forms.CharField(label='Номер телефона (950XXXXXXX)', help_text='Укажите номер телефона, без 8', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'on'}), max_length=10, required=True, validators=[validate_phone_isuse])
	
	captcha = CaptchaField(label='Проверка', )
	
	

def validate_password(value):
	p = re.compile('^\w*$')
	if not p.match(value):
		raise ValidationError(_(u'пароль должен состоять из символов английского алфавита.'))

class Form_change_password(forms.Form):
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','autocomplete': 'off'}), label=u'Пароль (новый)', min_length=6, max_length=100, required=True, validators=[validate_password])
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','autocomplete': 'off'}), label=u'Пароль (еще раз)', min_length=6, max_length=100, required=True, validators=[validate_password])
	
	def clean(self):
		cleaned_data = super(Form_change_password, self).clean()
		password = cleaned_data.get("password")
		password2 = cleaned_data.get("password2")
		if password != password2:
			msg = u'пароли не совпадают'
			self._errors['password'] = self.error_class([msg])
			self._errors['password2'] = self.error_class([msg])
			#del cleaned_data['password']
			#del cleaned_data['password2']
		return cleaned_data