# -*- coding: utf-8 -*-
# parsed_data/models.py
from django.db import models


class BlogData(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField(max_length=1000)

    def __str__(self):
    	return self.title