# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from users.models import User
from persons.models import Person
from photos.models import Photos
from django.contrib import admin

# Register your models here.
admin.site.register(User)
admin.site.register(Person)
admin.site.register(Photos)