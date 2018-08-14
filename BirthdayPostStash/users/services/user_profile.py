# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from users.models import UserProfile


class UserProfileService(object):
    def create_profile(self, user, **kwargs):
        date_of_birth = kwargs.get('date_of_birth')
        phone_ext = kwargs.get('phone_ext')
        phone_no = kwargs.get('phone_no')
        profile_picture = kwargs.get('profile_picture')
        profile = UserProfile(
            user=user,
            profile_picture=profile_picture,
            phone_ext=phone_ext,
            phone_no=phone_no,
            date_of_birth=date_of_birth
        )
        return profile
