from __future__ import unicode_literals

from rest_framework import serializers
from persons.models import Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('name', 'email', 'for_event', 'remind_on')
