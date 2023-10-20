# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255, default = "", unique=True)
    product_cost = models.CharField(max_length=20, default = "")
    product_type = models.CharField(max_length=255, default = "")    
    product_company = models.CharField(max_length=255, default = "")
    product_stock = models.CharField(max_length=255, default = "")	

    def __str__(self):
        return self.product_name