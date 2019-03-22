# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class Product(models.Model):
    product_id = models.IntegerField(primary_key=True,blank=False, null=False)
    description = models.CharField(max_length=128,blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True) # create
    updated_at = models.DateTimeField(auto_now=True) # save
    
    def __unicode__(self):
        return '%s: %s' % (self.product_id, self.description)

    class Meta:
        db_table = u'product'
        unique_together = (('description'),)
        verbose_name = 'Product Details'
        verbose_name_plural = 'Product Details'

class Tracking(models.Model):
    tracking_id = models.AutoField(primary_key=True)
    track_datetime = models.DateTimeField(default=timezone.now,blank=False, null=False,db_index=True)
    latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=False, null=False)
    longitude =  models.DecimalField(max_digits=22, decimal_places=16, blank=False, null=False)
    elevation = models.IntegerField(blank=False, null=False)
    product = models.ForeignKey(Product,related_name = 'tracking', unique=False)
    created_at = models.DateTimeField(default=timezone.now) # create
    updated_at = models.DateTimeField(auto_now=True) # save
    
    def __unicode__(self):
        return '%s: %s' % (self.product.description, self.track_datetime)

    class Meta:
        db_table = u'tracking'
        unique_together = (('product','track_datetime','latitude','longitude'),)
        verbose_name = 'Tracking Details'
        verbose_name_plural = 'Tracking Details'
