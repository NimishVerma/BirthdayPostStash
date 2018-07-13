# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import views, response, status, permissions
from photos.serializer import PhotoSerializer


class CreatePhoto(views.APIView):
    """
    End-Point to add photos
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):

        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(
                serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def pre_save(self, obj):
        obj.owner = self.request.user

