# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from albums.models import AlbumImage,People

admin.site.register(People)
admin.site.register(AlbumImage)