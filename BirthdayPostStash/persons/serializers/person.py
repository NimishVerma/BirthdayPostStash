# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from persons.models import Person


class PersonPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'
