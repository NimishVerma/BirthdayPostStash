from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager


class UserQuerySet(models.QuerySet):
    def exists_by_email(self, email):
        return self.filter(email=email).exists()

    def exists_by_username(self, username):
        return self.filter(username=username).exists()


class UserManager(BaseUserManager):

    def create_user(self, email, first_name=None,
                    last_name=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given email,
        password and name extra data
        """
        if not email:
            raise ValueError(_('Users must have a valid email address'))
        email = self.normalize_email(email).lower()
        if 'username' not in extra_fields:
            extra_fields['username'] = email
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name,
                         password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
            **extra_fields
        )
        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user