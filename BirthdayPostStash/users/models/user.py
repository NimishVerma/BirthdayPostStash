# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytz
import re
import uuid
from rest_framework.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin)
from users.managers import UserQuerySet, UserManager


class User(AbstractBaseUser, PermissionsMixin):

    """
    Custom User model
    -- Email is the Username field
    """
    email = models.EmailField(
        _("Email address"),
        max_length=254,
        null=True,
        blank=True,
        db_index=True)
    username = models.CharField(
        _("Username"),
        max_length=254,
        unique=True,
        db_index=True)
    first_name = models.CharField(
        _("First Name"),
        max_length=128,
        db_index=True)
    last_name = models.CharField(
        _("Last Name"),
        max_length=128,
        null=True,
        blank=True,
        db_index=True)
    unique_uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        db_index=True)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user \
            can log into this admin site."),
        db_index=True)

    is_active = models.BooleanField(
        _('active'),
        default=False,
        db_index=True,
        help_text=_("Designates whether this user \
            should be treated as active. \
            Unselect this instead of deleting accounts."))
    date_joined = models.DateTimeField(_('date joined'), default=now)

    objects = UserManager.from_queryset(UserQuerySet)()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "email",
        "first_name",
        "last_name",
    ]

    def set_password(self, password):
        match = re.search(
            "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[A-Za-z\d$@$!%*#?&]{6,123}$",
            password
        )
        if not match:
            raise ValidationError(
                detail={
                    "non_field_errors": [
                        "Password should have at least 6 characters, 1 capital alphabet and 1 numeric character."]
                },
                code=400
            )

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def get_by_id(self, id):
        return self.get(id=id)

    def get_full_name(self):
        return '{} {}'.format(
            self.first_name,
            self.last_name)

    def get_short_name(self):
        return '{}. {}'.format(
            self.first_name[0],
            self.last_name)

    def __unicode__(self):
        return "{}-{}".format(
            self.email, self.get_full_name())

    def __str__(self):
        return "{}-{}".format(
            self.email, self.get_full_name())
