# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from light_jets.models import Product, Tracking

admin.site.register(Product)
admin.site.register(Tracking)
