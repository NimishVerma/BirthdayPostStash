# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics, permissions
from ..serializers import PhotoSerializer, PhotoPublicSerializer
from ..models import Photos


class CreatePhoto(generics.CreateAPIView):
    """
    End-Point to add photos
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PhotoSerializer
    model = Photos


class ListPhoto(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PhotoPublicSerializer
    model = Photos

    def get_queryset(self):
        return self.model.objects.all()


class ListPhotosByPerson(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PhotoPublicSerializer
    model = Photos

    def get_queryset(self):
        return self.model.objects.filter(participants)
