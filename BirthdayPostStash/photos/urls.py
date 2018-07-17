# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from .apis import *

urlpatterns = [
    url(r'^create-photo/',
        CreatePhoto.as_view(),
        name="api_create_photo"),
    url(r'^list-photo/',
        ListPhoto.as_view(),
        name="api_list_photo"),
]
