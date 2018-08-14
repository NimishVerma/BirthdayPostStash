# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from django.utils import timezone
from users.models import UserProfile
from users.services import UserProfileService


class UserProfileSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if not data.get('date_of_birth'):
            raise serializers.ValidationError(
                'Please provide a valid birthdate')
        if data.get('date_of_birth') > timezone.now().date():
            raise serializers.ValidationError(
                'Please provide a valid birthdate')
        try:
            profile = UserProfile.objects.get(
                user=self.context.get('request').user)
        except:
            profile = None
        if profile:
            raise serializers.ValidationError('Profile already setup')

        return data

    def create(self, validated_data):
        logged_in_user = self.context.get('request').user
        profile_service = UserProfileService()
        profile = profile_service.create_profile(
            user=logged_in_user,
            profile_picture=validated_data.get('profile_picture'),
            date_of_birth=validated_data.get('date_of_birth'),
            phone_ext=validated_data.get('phone_ext', None),
            phone_no=validated_data.get('phone_no', None))
        profile.save()
        return profile

    class Meta:
        model = UserProfile
        exclude = 'user',
