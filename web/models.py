# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Tip(models.Model):
    subject = models.CharField(max_length=100)
    text = models.TextField()
    directed_to = models.CharField(max_length=100, null=True, blank=True)
    submitted_on = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    response = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.subject