# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from users.models import User
from persons.models import Person


def get_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex, ext)
    return os.path.join('photos', str(instance.id), filename)


class Photos(models.Model):

    owner = models.ForeignKey(
        User,
        related_name="photos_owner")
    photo = models.ImageField(
        upload_to=get_image_path, blank=True)
    participants = models.ManyToManyField(
        Person,
        related_name="photos_participants",
        null=True,
        blank=True)
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

    class Meta:
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')

    def __unicode__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)
