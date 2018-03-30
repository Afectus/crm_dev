# -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group

from rest_framework import serializers
from rest_framework import viewsets, generics, permissions

from .models import *
from node.models import *




class buyerauth_serializers(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = buyer
		fields = ('id', 'authtoken', 'phone', )


	
	
class buyerauthtesttoken(generics.RetrieveAPIView):
    lookup_field = "authtoken"
    queryset = buyer.objects.all()
    serializer_class = buyerauth_serializers
	
'''		
class discounts_ViewSet(viewsets.ModelViewSet):
    queryset = discounts.objects.all()
    serializer_class = discounts_serializers
		
	
class goodslist(generics.ListCreateAPIView):
    queryset = discounts.objects.all()
    serializer_class = discounts_serializers
    #permission_classes = (IsAdminUser,)
	
class goodscreate(generics.CreateAPIView):
    #queryset = discounts.objects.all()
    serializer_class = discounts_serializers
    #permission_classes = (IsAdminUser,)
'''