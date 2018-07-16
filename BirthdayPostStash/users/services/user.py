# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import string
import random
from django.contrib.auth import get_user_model

from users import settings as accounts_settings

User = get_user_model()


class UserService(object):
    """
    Business layer around User entity
    """

    def make_random_password(self):
        return (
            ''.join(random.choice(
                string.ascii_uppercase
            ) for _ in range(3))) + (
            ''.join(random.choice(string.digits) for _ in range(3))) + (
            ''.join(random.choice(string.ascii_lowercase) for _ in range(3)))

    def create_user(self, **kwargs):
        """
        Create new User instance with appropriate attributes.

        :param first_name(mandatory): first_name
        :param email(optional): email address
        :param last_name(optional): last_name
        :param username(optional): username - default to email.
        :param password(optional): password - default random generated.

        **Then**
            - verify email is mandatory
            - normalize email, lowercase it
            - normalize names
            - If no username provided - assign email as username
            - create a new user instance
            - If given password - validate
            - If no password provided - generate a random password
            - set its password & name correctly
            - Mark him active only when Activation is set to False

        :returns: a new User model instance

        :raises AssetError: Name is not specified.
        """
        email = kwargs.get('email', '')
        first_name = kwargs.get('first_name')
        last_name = kwargs.get('last_name', '')
        assert first_name
        username = (kwargs.get('username', email)).lower()
        if email:
            email = User.objects.normalize_email(email).lower()
        user = User(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name)
        password = kwargs.get(
            'password',
            self.make_random_password())
        user.set_password(password)
        if not accounts_settings.get('SEND_ACTIVATION_EMAIL'):
            user.is_active = True
        return user

    def verify_account(self, user, password):
        """
        Verify user account for Authentication.

        :param user(mandatory): user
        :param password(mandatory): password

        **Then**
            - check password and is_active to verify user

        :returns: user credentials verification
        """
        if user.check_password(password) and user.is_active:
            return True
        return False

    def update_user(self, user, **kwargs):
        """
        Update User instance

        :param user(mandatory): user
        :param email(optional): email
        :param username(optional): username
        :param first_name(optional): first_name
        :param last_name(optional): last_name

        **Then**
            - update email to user instance.
            - update username to user instance.
            - update name to user instance.
            - mark user active accordingly.

        :returns: user instance
        """
        email = kwargs.get('email')
        username = kwargs.get('username').lower()
        first_name = kwargs.get('first_name')
        is_active = kwargs.get('is_active', None)
        if email and user.email != email:
            user.email = email
            if accounts_settings.get('SET_USER_INACTIVE_EMAIL_CHANGE'):
                user.is_active = False
        if username and user.username != username:
            user.username = username
            if accounts_settings.get('SET_USER_INACTIVE_USERNAME_CHANGE'):
                user.is_active = False
        if first_name:
            user.first_name = first_name
        if is_active is not None:
            user.is_active = is_active
        user.last_name = kwargs.get('last_name', '')
        user.timezone = kwargs.get('timezone', user.timezone)
        return user

    def update_user_from_vendor(self, user, **kwargs):
        username = kwargs.get('username').lower()
        email = kwargs.get('email', user.email)

        if email and user.email != email:
            if accounts_settings.get('SET_USER_INACTIVE_EMAIL_CHANGE'):
                user.is_active = False
        if username and user.username != username:
            user.username = username
            if accounts_settings.get('SET_USER_INACTIVE_USERNAME_CHANGE'):
                user.is_active = False
        user.email = email.lower() if email else ""
        user.first_name = kwargs.get('first_name', user.first_name)
        user.last_name = kwargs.get('last_name', user.last_name)
        user.is_active = kwargs.get('is_active', user.is_active)
        user.timezone = kwargs.get('timezone', user.timezone)
        return user

    def change_password(self, user, password):
        """
        Update user instance password.

        :param user(mandatory): user
        :param password(mandatory): password

        **Then**
            - Update User password.
            - mark user active accordingly.

        :returns: user instance
        """
        user.set_password(password)
        if accounts_settings.get('SET_USER_INACTIVE_PASSWORD_CHANGE'):
            user.is_active = False
        return user

    def activate_user(self, user):
        """
        Update user instance to active.

        :param user(mandatory): user

        **Then**
            - Update User is_active.

        :returns: user instance
        """
        user.is_active = True
        return user
