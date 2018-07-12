# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from .apis import *

urlpatterns = [
    url(r'^create-photo/',
        CreatePhoto,
        name="api_create_photo"),
]
