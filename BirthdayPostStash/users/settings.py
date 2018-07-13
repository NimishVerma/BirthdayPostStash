# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext as _

from rest_framework import serializers


def regex_validator(value):
    match = re.search("^(?=.*[a-z])(?=.*[A-Z])[A-Za-z\d$@$!%*#?& ]{6,123}$", value)
    if not match:
        raise serializers.ValidationError(
            _("Password should have atleast 6 characters, 1 capital alphabet and 1 numeric character")
        )

default_settings = {
    'SEND_ACTIVATION_EMAIL': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'SET_PASSWORD_RETYPE': True,
    'SET_USER_INACTIVE_EMAIL_CHANGE': False,
    'SET_USER_INACTIVE_USERNAME_CHANGE': False,
    'SET_USER_INACTIVE_PASSWORD_CHANGE': False,
    'PASSWORD_VALIDATORS': [regex_validator,],
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
}


def get(key):
    try:
        return default_settings[key]
    except KeyError:
        raise ImproperlyConfigured(
            'Missing settings: default_settings[\'{}\']'.format(key))
