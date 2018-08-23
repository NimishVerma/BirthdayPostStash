# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils import timezone
import django.contrib.auth.password_validation as validators


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
        )
        read_only_fields = ('is_active', 'auth_token',)

    def create(self, validated_data):
        user_service = UserService()
        user = user_service.create_user(**validated_data)
        user.is_active = True
        user.save()
        return user

    def validate_email(self, email):
        email = email.lower()
        if email:
            if User.objects.exists_by_email(email):
                raise serializers.ValidationError(
                    messages.EMAIL_EXISTS_ERROR)
        return email

    def validate_password(self, password):
        validators.validate_password(password=password)
        return password

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


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer User login

    **Validate**
        - validate user exists with given username
        - Use UserService to verify credentials.

    **Create**
        - None
    """

    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None
        self.fields[User.USERNAME_FIELD] = serializers.CharField()

    password = serializers.CharField(
        style={'input_type': 'password'})

    def validate(self, data):
        username = data.get(User.USERNAME_FIELD).lower()
        password = data.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            raise serializers.ValidationError(
                messages.INVALID_CREDENTIALS_ERROR)
        data['user'] = user
        user_service = UserService()
        is_valid = user_service.verify_account(user, password)
        if not is_valid:
            raise serializers.ValidationError(
                messages.INACTIVE_ACCOUNT_ERROR)
        return data

    class Meta:
        fields = (User.USERNAME_FIELD, 'password')
