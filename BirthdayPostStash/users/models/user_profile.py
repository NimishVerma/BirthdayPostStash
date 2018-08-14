# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import uuid

from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from users.models import User


def get_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex, ext)
    return os.path.join('profile', str(instance.id), filename)


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        related_name="user_profile_user"
    )
    profile_picture = models.ImageField(
        upload_to=get_image_path, blank=True)
    phone_ext = models.CharField(
        _('Calling Code'),
        max_length=4,
        validators=[
            RegexValidator(
                regex='^\+([0-9]{1,3})$',
                message="Calling code can only contain '+' and '0-9' numeric values",
                code='invalid_calling_code'
            ),
        ],
        null=True,
        blank=True,
    )
    phone_no = models.CharField(
        _('Phone Number'),
        max_length=11,
        validators=[
            RegexValidator(
                regex='^([0-9]{10,11})$',
                message="""Phone number must be 10-11 digits.""",
                code='invalid_phone_number'
            ),
        ],
        null=True,
        blank=True,
    )
    date_of_birth = models.DateField(
        _("date_of_birth"),
        db_index=True)
