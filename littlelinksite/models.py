# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class LittleLinkUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Shorturl(models.Model):
    new_url_id = models.SlugField(max_length=50, primary_key=True)
    orig_url = models.URLField(max_length=2083) # IE Maximum URL length
    no_clicks = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published', auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, default=None)

    def __str__(self):
        return self.orig_url