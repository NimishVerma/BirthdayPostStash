# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models.signals import post_save
from django.db import models
from django.utils.translation import ugettext_lazy as _
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
    create_date = models.DateTimeField(
        _("Created At"),
        auto_now_add=True)
    modified_date = models.DateTimeField(
        _("Modified At"),
        auto_now=True,
        db_index=True)
    is_deleted = models.BooleanField(
        _("Is Instance marked deleted"),
        default=False)
    is_active = models.BooleanField(
        _("Is Instance marked Active"),
        default=True,
        db_index=True)

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)
