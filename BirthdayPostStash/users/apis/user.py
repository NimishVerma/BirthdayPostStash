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
    """
    Use this endpoint to register new User.

    **Url**
        ``/users/register/``

    **Permissions**
        - Any is allowed.

    **After Save**
        - Save User instance
        - Generate Activation token and add it to response.

    **finalize_response**
        - create token and set it into cookie
    """
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
        serializer.save


class UserLogin(generics.GenericAPIView):
    """
    Use this end-point to authenticate a user and generate an auth token.

    **Url**
        ``/users/login/``

    **Permissions**
        - Any is allowed.

    **Post**
        - Validate via Serializer
        - Generate Auth Token

    **Finalize Response**
        - From database get or create an auth token.
        - Set authorization into cookie with finalize_response.
    """
    serializer_class = serializers.UserLoginSerializer
    permission_classes = (
        permissions.AllowAny,
    )

    def finalize_response(self, request, *args, **kwargs):
        """
        Set Authorization in cookie.
        """
        response_obj = super(UserLogin, self).finalize_response(
            request, *args, **kwargs)
        if request.POST and response_obj.status_code == 200:
            response_obj['Authorization'] = 'Token '\
                + response_obj.data['auth_token']
            response_obj.set_cookie(
                'Authorization', response_obj['Authorization'])
        return response_obj

    def post(self, request):
        """
        If serializer is valid.
            - call action.
        """
        serializer = self.get_serializer(
            data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            token, boolean = Token.objects.get_or_create(user=user)
            token.save()
            user.login_attempts = 0
            user.save()
            data = serializers.TokenSerializer(token).data
            return response.Response(
                data=data,
                status=status.HTTP_200_OK,)
        return response.Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)
