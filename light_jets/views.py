# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.generic import CreateView
from light_jets.models import Product, Tracking
from rest_framework import generics, permissions
from rest_framework import status as http_status
from rest_framework import viewsets
from rest_framework.response import Response
from serializers import ProductSerializer, TrackingSerializer


@login_required
def jets(request):
    """
    Jets page
    """
    jets = Product.objects.all().order_by('product_id')
    serializer = ProductSerializer(jets,many=True).data
    return render_to_response('light_jets/jets.html',
                                {'data': serializer},
                             )


@login_required
def tracking(request):
    """
    Default/Tracking Landing page
    """
    track = Tracking.objects.all().order_by('product_id')
    serializer = TrackingSerializer(track,many=True).data
    return render_to_response('light_jets/home.html',
                                {'data': serializer},
                              )

@login_required
def upload(request):
    """
    Upload sample data
    """
    return render_to_response('light_jets/upload.html')

@login_required
def maps(request):
    """
    Interactive Map of Tracking the Jets
    """
    return render_to_response('light_jets/maps.html')



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get', 'post', 'head', 'put','patch','delete']
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # POST for handling one/multiple products
    def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list)) # one/many entries
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=http_status.HTTP_201_CREATED, headers=headers)     

class TrackingViewSet(viewsets.ModelViewSet):
    queryset = Tracking.objects.all()
    serializer_class = TrackingSerializer
    http_method_names = ['get', 'post', 'head', 'put','patch','delete']
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # POST for handling one/multiple products
    def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
            is_true = serializer.is_valid() # not throwing exception here
            special = False
            # serialization.errors custom handling 
            if not is_true:
                # multiple trackings in payload
                if isinstance(serializer.errors,list):
                    errors = serializer.errors 
                    for v in errors:
                        for k,m in v.items():
                            if isinstance(m,dict):
                                for j,l in m.items():
                                    if l[0].find('Product Details with this product id already exists') >=0:
                                        special = True
                                    else:
                                        serializer.is_valid(raise_exception=True)
                            else:
                                if m[0].find('Product Details with this product id already exists') >=0:
                                    special = True
                                else:
                                    serializer.is_valid(raise_exception=True)
                # One tracking in payload
                else:
                    errors = serializer.errors.values()
                    for v in errors:
                        if isinstance(v,dict):
                            for k,m in v.items():
                                if m[0].find('Product Details with this product id already exists') >=0:
                                    special = True
                                else:
                                    serializer.is_valid(raise_exception=True)
                        else:
                            if v[0].find('Product Details with this product id already exists') >=0:
                                special = True
                            else:
                                serializer.is_valid(raise_exception=True)

            if special:
                data = self._perform_create(serializer.initial_data)
            else:
                data = self._perform_create(serializer.validated_data)
                
            headers = self.get_success_headers(data)
            return Response(data, status=http_status.HTTP_201_CREATED, headers=headers)

    def _perform_create(self, data):
        """
        Overriding perform_create to handle custom behavior of handling existing Product objects.
        """
        if isinstance(data,list):
            for each in data:
                self._product_update_create(each)
        else:
            self._product_update_create(data)
        return data

    def _product_update_create(self,data):
        product_data = data.pop('product')
        product_obj, created = Product.objects.get_or_create(**product_data)
        if created:
            product_obj.save() 
        data['product'] = product_obj
        if 'tracking_id' in data.keys():
            data.pop('tracking_id')
        Tracking.objects.update_or_create(**data)
        data['product'] = product_data # For serializer
        return data
    
    # PUT, PATCH
    def update(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data, many=False) # PUT/PATCH for only one entity
            serializer.is_valid()
            is_true = serializer.is_valid()
            special = False
            if not is_true:
                # multiple trackings in payload
                if isinstance(serializer.errors,list):
                    errors = serializer.errors
                    for v in errors:
                        for k,m in v.items():
                            for j,l in m.items():
                                if l[0].find('Product Details with this product id already exists') >=0:
                                    special = True
                                else:
                                    serializer.is_valid(raise_exception=True)
                # One tracking in payload
                else:
                    errors = serializer.errors.values()
                    for v in errors:
                        if isinstance(v,dict):
                            for k,m in v.items():
                                if m[0].find('Product Details with this product id already exists') >=0:
                                    special = True
                                else:
                                    serializer.is_valid(raise_exception=True)
                        else:
                            if v[0].find('Product Details with this product id already exists') >=0:
                                special = True
                            else:
                                serializer.is_valid(raise_exception=True)
            if special:
                data = self._perform_create(serializer.initial_data)
            else:
                data = self.perform_create(serializer)

            headers = self.get_success_headers(serializer.data)
            return Response(data, status=http_status.HTTP_202_ACCEPTED, headers=headers)
