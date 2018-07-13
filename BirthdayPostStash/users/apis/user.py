# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

# Core Python & django imports at top
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from django.contrib.auth.models import Group

# Third party lib imports
from rest_framework import permissions, generics, response, status, views
from rest_framework.authtoken.models import Token

from users import (
    serializers, messages,
    settings as accounts_settings,
    services)

User = get_user_model()


class UserRegister(generics.CreateAPIView):

    serializer_class = serializers.UserRegisterSerializer
    permission_classes = (
        permissions.AllowAny,
    )

    def finalize_response(self, request, *args, **kwargs):
        """
        Set Authorization in cookie.
        """
        response_obj = super(UserRegister, self).finalize_response(
            request, *args, **kwargs)
        if not hasattr(response_obj.data, 'username'):
            return response_obj
        if request.POST:
            user = User.objects.get_by_username(
                response_obj.data.get('username'))
            token, boolean = Token.objects.get_or_create(user=user)
            response_obj['Authorization'] = 'Token '\
                + str(token)
            response_obj.set_cookie(
                'Authorization', response_obj['Authorization'])
        return response_obj

    def perform_create(self, serializer):
        serializer.save()
