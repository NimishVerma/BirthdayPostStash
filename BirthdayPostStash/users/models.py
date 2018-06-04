# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models.signals import post_save
from django.db import models
from django.db.models.signals import post_save 
from django.dispatch import Signal
from django import forms
from django.contrib.auth.models import User
import os

def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    profile_image = models.ImageField(upload_to=get_image_path, blank=True)

    def __str__(self):
    	return self.user.username

def create_profile(sender, **kwargs):
	if kwargs['created']:
		user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile,sender=User)