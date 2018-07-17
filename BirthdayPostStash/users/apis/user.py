# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

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
        serializer.save()


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
            if not boolean:
                token.created = datetime.datetime.now()
                token.save()
            # user.login_attempts = 0
            user.save()
            data = serializers.TokenSerializer(token).data
            return response.Response(
                data=data,
                status=status.HTTP_200_OK,)
        return response.Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)


class UserLogout(views.APIView):
    """
    **Use this endpoint to logout user (remove user authentication token)**.

    Url:
        ``/users/logout/``

    Permissions:
        * Only authenticated Users

    **Post**
        - Delete Auth token
    """
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request):
        Token.objects.filter(user=request.user)
        return response.Response(
            data=messages.LOG_OUT_SUCCESS,
            status=status.HTTP_200_OK)

# TODO Fix Bug HTTP:500


class GetToken(views.APIView):
    """
    Use this end-point to get an auth token.

    **Url**
        ``/t2b/accounts/get-token/``

    **Permissions**
        - Any is allowed.

    **Get**
        - From database get an auth token.

    """
    permission_classes = (
        permissions.AllowAny,
    )

    def get(self, request):
        """
        If serializer is valid.
            - call action.
        """
        unique_uuid = self.request.META.get(
            'HTTP_UNIQUEUUID')
        a = request.COOKIES.get('Authorization')
        print a
        data = {}
        if unique_uuid:
            user = User.objects.filter(unique_uuid=unique_uuid)
            if user:
                token, boolean = Token.objects.get_or_create(
                    user=user.first())
                token.save()
                data = serializers.TokenSerializer(token).data
                return response.Response(
                    data=data,
                    status=status.HTTP_200_OK,
                )
        return response.Response(
            data=data,
            status=status.HTTP_400_BAD_REQUEST)
