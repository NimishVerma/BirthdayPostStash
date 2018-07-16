# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from photos.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('owner', 'participants')
