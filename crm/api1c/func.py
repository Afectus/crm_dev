# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponsePermanentRedirect

from django.core.exceptions import PermissionDenied


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

import datetime, time

from django.db.models import Sum, Count
from django.db.models import Q

from django.views.decorators.csrf import csrf_exempt

#from node.templatetags.nodetags import node_count

from django.conf import settings

from node.models import *
from dj.views import *

import xlwt #import module excel
from PyPDF2 import PdfFileMerger
import os

import hashlib
import random

import logging
log = logging.getLogger(__name__)

urlprefix = 'http://crm.babah24.ru/'
root = '/var/www/crm/'



#генератор случайностей
def id1c_generator(size=7):
	#chars=string.letters + string.digits
	chars=string.digits
	return ''.join(random.choice(chars) for _ in range(size))


def makeapitoken_1c(salt):
	apitoken=settings.MAKEAPITOKEN_1C_TOKEN
	crc = hashlib.md5()
	crc.update(('%s:%s' % (salt, apitoken)).encode('utf-8'))
	crc=crc.hexdigest()
	return crc.upper()





def makecertpdf(data, pdffile):
	merger = PdfFileMerger(strict=False)
	merger.append(pdffile)
	for i in data:
		if i.goodscert:
			#print i.goodscert.pdf.path
			merger.append(i.goodscert.pdf.path)
		# else: #если нет сертификата, то поиск во второй базе
			# try:
				# r=relgoods.objects.get(b=i)
			# except:
				# pass
			# else:
				# log.info('makecertpdf=%s' % r.a)
				# log.info('makecertpdf=%s' % r.a.goodscert)
				# if r.a.goodscert:
					# merger.append(r.a.goodscert.pdf.path)
				# else:
					# pass

	pdfout = "media/CACHE/%s.pdf" % (id_generator())

	merger.write('%s%s' % (root, pdfout))

	pdfurl = '%s%s' % (urlprefix, pdfout)
	return pdfurl



def makecertexcel(head, data, pdfurl=None):
	#create excel book
	wb = xlwt.Workbook()
	ws = wb.add_sheet('main')
	
	ws.header_str = ''
	ws.footer_str = ''
	
	font_style='Arial'

	# #default start settings
	down = 0
	row = 3

	#############################
	#fnt = xlwt.Font()
	#fnt.name = font_style
	#fnt.bold = True
	#borders = xlwt.Borders()
	#borders.left = xlwt.Borders.THIN
	#borders.right = xlwt.Borders.THIN
	#borders.top = xlwt.Borders.THIN
	#borders.bottom = xlwt.Borders.THIN
	#al = xlwt.Alignment()
	#al.horz = xlwt.Alignment.HORZ_CENTER
	#al.vert = xlwt.Alignment.VERT_CENTER
	#style = xlwt.XFStyle()
	#style.font = fnt
	#style.borders = borders
	#style.alignment = al
	style = xlwt.easyxf('font: name Arial, height 180, bold on, color-index black; alignment: horiz center;')
	#ws.write_merge(marginbottom,mergebottom,marginleft, mergeright, u'тест', style)
	ws.write_merge(down, 0, 0, row, head, style) #объединить ячейки

	##################################
	down = down + 1
	#fnt = xlwt.Font()
	#fnt.name = font_style
	#fnt.bold = True
	#borders = xlwt.Borders()
	#borders.left = xlwt.Borders.THIN
	#borders.right = xlwt.Borders.THIN
	#borders.top = xlwt.Borders.THIN
	#borders.bottom = xlwt.Borders.THIN
	#al = xlwt.Alignment()
	#al.horz = xlwt.Alignment.HORZ_JUSTIFIED
	#al.vert = xlwt.Alignment.VERT_CENTER
	#style = xlwt.XFStyle()
	#style.font = fnt
	#style.borders = borders
	#style.alignment = al
	style = xlwt.easyxf('font: name Arial, height 180, color-index black; alignment: horiz justified, vertical center, indent 1;')
	ws.row(down).height = 1400 #высота ячейки
	#ws.write_merge(marginbottom,mergebottom,marginleft, mergeright, u'тест', style)
	ws.write_merge(down, down, 0, row, u'Настоящий товарно-сопроводительный документ подготовлен в соответствии с постановлением правительства РФ от 19.01.98 г. № 56 "Об утверждении правил продажи отдельных видов товаров". При продаже товаров, подлежащих обязательной сертификации, продавец доводит до сведения покупателя через товарно-сопроводительные документы, оформленные на основании подлинника сертификата с указанием его номера, срока действия и органа, выдавшего сертификат. Сведения о сертификации должны быть заверены подписью и печатью изготовителя (поставщика, продавца) с указанием телефона."', style) #объединить ячейки
	
	###################################
	down = down + 2
	#fnt = xlwt.Font()
	#fnt.name = font_style
	#fnt.bold = True
	#borders = xlwt.Borders()
	#borders.left = xlwt.Borders.THIN
	#borders.right = xlwt.Borders.THIN
	#borders.top = xlwt.Borders.THIN
	#borders.bottom = xlwt.Borders.THIN
	#al = xlwt.Alignment()
	#al.horz = xlwt.Alignment.HORZ_CENTER
	#al.wrap = xlwt.Alignment.WRAP_AT_RIGHT
	#al.vert = xlwt.Alignment.VERT_CENTER
	#style = xlwt.XFStyle()
	#style.font = fnt
	#style.borders = borders
	#style.alignment = al
	style = xlwt.easyxf('font: name Arial, height 160, bold on, color-index black; alignment: horiz center, vertical center; borders: top thin, bottom thin, right thin, left thin;')
	ws.write(down, 0, u'Номенклатура', style)
	ws.write(down, 1, u'Номер', style)
	ws.write(down, 2, u'Дата сертификата', style)
	ws.write(down, 3, u'Орган, выдавший сертификат', style)

	for i in range(row+1): #пробежимся по колонкам и устновим ширину столбца
		ws.col(i).width = 6000 #ширина столбца
		ws.row(i).height_mismatch = True
		#ws.row(i).height = 1000
	
	######################################
	down = down + 1
	#fnt = xlwt.Font()
	#fnt.name = font_style
	#al = xlwt.Alignment()
	#al.wrap = xlwt.Alignment.WRAP_AT_RIGHT
	#al.horz = xlwt.Alignment.HORZ_CENTER
	#al.vert = xlwt.Alignment.VERT_CENTER
	#borders = xlwt.Borders()
	#borders.left = xlwt.Borders.THIN
	#borders.right = xlwt.Borders.THIN
	#borders.top = xlwt.Borders.THIN
	#borders.bottom = xlwt.Borders.THIN
	#style = xlwt.XFStyle()
	#style.font = fnt
	#style.borders = borders
	#style.alignment = al
	style0 = xlwt.easyxf('font: name Arial, height 160, color-index black; alignment: horiz justified, vertical center, indent 1; borders: top thin, bottom thin, right thin, left thin;')
	style1 = xlwt.easyxf('font: name Arial, height 160, color-index black; alignment: horiz center, vertical center; borders: top thin, bottom thin, right thin, left thin;')

	for i in data:
		#ws.row(i).height_mismatch = True
		ws.row(down).height = 500
		ws.write(down, 0, i.name, style0)
		if i.goodscert:
			ws.write(down, 1, i.goodscert.name, style1)
			ws.write(down, 2, '%s - %s' % (i.goodscert.datestart.strftime('%d.%m.%Y'), i.goodscert.dateend.strftime('%d.%m.%Y')), style1)
			ws.write(down, 3, i.goodscert.org, style1)
		else:
			ws.write(down, 1, u'Нет', style1)
			ws.write(down, 2, u'Нет', style1)
			ws.write(down, 3, u'Нет', style1)
		down=down+1
		
	
	############################
	down = down + 1	
	#fnt = xlwt.Font()
	#fnt.name = font_style
	#al = xlwt.Alignment()
	#al.vert = xlwt.Alignment.VERT_CENTER
	#style = xlwt.XFStyle()
	#style.font = fnt
	#style.alignment = al
	#ws.write_merge(marginbottom,mergebottom,marginleft, mergeright, u'тест', style)
	style = xlwt.easyxf('font: name Arial, height 180, color-index black; alignment: horiz justified, vertical center, indent 1;')
	ws.write_merge(down, down, 0, row, u'В случае если окончание срока действия не указано, сертификат является бессрочным.', style) #объединить ячейки
	
	if pdfurl: #если есть PDF дописываем
		#
		down = down + 2	
		#	

		fnt = xlwt.Font()
		fnt.name = font_style
		fnt.bold = True
		al = xlwt.Alignment()
		al.wrap = xlwt.Alignment.WRAP_AT_RIGHT
		al.horz = xlwt.Alignment.HORZ_CENTER
		al.vert = xlwt.Alignment.VERT_CENTER
		style = xlwt.XFStyle()
		style.font = fnt
		style.alignment = al
		style.font.colour_index = xlwt.Style.colour_map['blue']
		#ws.write_merge(marginbottom,mergebottom,marginleft, mergeright, u'тест', style)
		ws.write_merge(down, down, 0, row, xlwt.Formula(u'HYPERLINK("%s";"Скачать сертификаты в PDF")' % pdfurl), style) #объединить ячейки
	
	#
	
	# default_book_style = wb.default_style
	# default_book_style.font.height = 20 * 36    # 36pt
	
	
	filename = id_generator()
	xlsout = 'media/CACHE/%s.xls' % (filename)
	pdfout = 'media/CACHE/%s.pdf' % (filename)
	xlsurl = '%s%s' % (urlprefix, xlsout)
	xlspath = '%s%s' % (root, xlsout)

	wb.save(xlspath)
	
	#convert xls to pdf via libreoffice
	os.system('/usr/bin/libreoffice libreoffice --headless --convert-to pdf --outdir /var/www/crm/media/CACHE %s' % (xlspath));
	pdfpath = '%s%s' % (root, pdfout)
	
	return (xlsurl, xlspath, pdfpath)
	
	
	