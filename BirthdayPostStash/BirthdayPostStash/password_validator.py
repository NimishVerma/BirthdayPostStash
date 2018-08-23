# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CustomPasswordValidator(object):
    def __init__(self, expression="^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[A-Za-z\d$@$!%*#?&]{6,123}$"):
        self.expression = expression

    def validate(self, password, user=None):
        match = re.search(self.expression, password)
        if not match:
            raise ValidationError(
                _("Password should have at least 6 characters, 1 capital alphabet and 1 numeric character")
            )

    def get_help_text(self):
        return _("Password should have at least 6 characters, 1 capital alphabet and 1 numeric character")
