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
	


	

