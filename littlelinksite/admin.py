# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Shorturl


class ShorturlAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['orig_url']}),
        ('Date information',    {'fields': ['pub_date']})
    ]

    readonly_fields=('pub_date',)
    list_display = ('orig_url', 'new_url_id', 'no_clicks', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['orig_url']

admin.site.register(Shorturl, ShorturlAdmin)