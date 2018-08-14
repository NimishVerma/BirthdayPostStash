# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import (
    permissions, generics,
    status, response
)
from users import serializers
from users.models import UserProfile


class SetupUserProfile(generics.CreateAPIView):

    serializer_class = serializers.UserProfileSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    model = UserProfile

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(
            data=request.data, context={
                'view': self,
                'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(
                data='success', status=status.HTTP_201_CREATED)

        return response.Response(
            data={'detail': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST)


class GetUserProfile(generics.RetrieveAPIView):
    serializer_class = serializers.UserProfileSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    model = UserProfile
    lookup_field = 'username'
    def get_object(self):
	key = self.kwargs.get('username')
        return self.model.objects.get(user__username=key)
