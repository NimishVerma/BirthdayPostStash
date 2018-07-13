# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils import timezone

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from users import settings as accounts_settings
from users.models import User
from users.services import UserService
from users import messages


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer User registration

    **Validate**
        - Email exists or not in database.

    **Create**
        - Use UserService to create_user.
        - Save new user instance to database.
    """
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        validators=accounts_settings.get('PASSWORD_VALIDATORS'))

    auth_token = serializers.SerializerMethodField()

    company_name = serializers.CharField(write_only=True)

    def get_auth_token(self, obj):
        token, boolean = Token.objects.get_or_create(user=obj)
        return TokenSerializer(token).data.get('auth_token')

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            User.USERNAME_FIELD,
            User._meta.pk.name,
            'password', 'is_active',
            'auth_token',
            'company_name'
        )
        read_only_fields = ('is_active', 'auth_token',)

    def create(self, validated_data):
        user_service = UserService()
        user = user_service.create_user(**validated_data)
        user.extra_data = [
            {'company_name': validated_data.get('company_name')}
        ]
        user.save()
        return user

    def validate_email(self, email):
        email = email.lower()
        if email:
            if User.objects.exists_by_email(email):
                raise serializers.ValidationError(
                    messages.EMAIL_EXISTS_ERROR)
        return email

    def validate_username(self, username):
        username = username.lower()
        if User.objects.exists_by_username(username):
            raise serializers.ValidationError(
                messages.USERNAME_EXISTS_ERROR)
        return username


class TokenSerializer(serializers.ModelSerializer):
    """
    returns auth token for the login user
    """
    auth_token = serializers.CharField(source='key')

    class Meta:
        model = Token
        fields = ('auth_token',)
