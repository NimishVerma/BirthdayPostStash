# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from rest_framework import serializers
from ..models import Photos
from .. import messages
from persons.serializers import PersonPublicSerializer


class PhotoSerializer(serializers.ModelSerializer):
    def validate(self, data):
        filename, file_extension = os.path.splitext(
            data.get('photo').name)
        accepted_images = [".jpg", ".jpeg", ".svg", ".png"]
        if file_extension not in accepted_images:
            raise serializers.ValidationError(
                messages.INVALID_IMAGE)
        return data

    def create(self, validated_data):
        owner = self.context.get('view').request.user
        instance = Photos(
            photo=validated_data.get('photo'),
            is_active=True,
            owner=owner,
        )
        instance.save()
        instance.participants = validated_data.get('participants')
        instance.save()
        return instance

    class Meta:
        model = Photos
        exclude = ('owner', 'is_active', 'is_deleted')


class PhotoPublicSerializer(serializers.ModelField):
    participants = PersonPublicSerializer(many=True)

    class Meta:
        model = Photos
        fields = '__all__'
