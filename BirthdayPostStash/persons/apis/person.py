from __future__ import unicode_literals

import operator
from rest_framework import generics, views, response, status, permissions
from persons.serializers import PersonPublicSerializer

from persons.models import Person
from photos.models import Photos

class CreatePerson(views.APIView):
    """
    End point to add Persons
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = PersonPublicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(
                serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def pre_save(self, obj):
        obj.created_by = self.request.user


class GetPersonsByUser(views.APIView):
    """
    End point to get all friends of a user
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        queryset = Person.objects.filter(created_by=user)
        return queryset


class GetTopFive(generics.ListAPIView):
    """
    End point to get top 5 friends
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PersonPublicSerializer 
    model = Person
    def get_queryset(self):
	all_friends = []
	top_friends = {}
        all_friends = self.model.objects.filter(created_by=self.request.user)
        if all_friends:
	    for friend in all_friends:
		photos = []
                photos = Photos.objects.filter(participants__in=friend)
		if photos:
		    top_friends[friend] = len(photos)

        if top_friends:
	    sorted_x = sorted(ids.items(), key=operator.itemgetter(1), reverse=True)
            top_five = dict(sorted_x[:5]).keys()
	    return self.model.objects.filter(id__in=top_five)
	return self.model.objects.none()

	     

