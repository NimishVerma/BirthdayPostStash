# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.db import models

# Create your models here.
from users.models import User

from django.utils.translation import ugettext_lazy as _


class Person(models.Model):
    name = models.CharField(
        max_length=25,
        default='John Doe',
        blank=True,
        db_index=True)
    email = models.EmailField(
        unique=False,
        blank=True)
    for_event = models.CharField(
        max_length=20,
        blank=False)
    remind_on = models.DateField(
        _("date to be reminded on"),
        blank=False,)
    created_by = models.ForeignKey(
        User,
        related_name='person_creator')
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
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __unicode__(self):
        return str(self.name)

    def __str__(self):
        return str(self.id + '|' + self.created_by)
