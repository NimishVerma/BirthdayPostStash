from __future__ import unicode_literals

from rest_framework import views, response, status, permissions
from pesons.serializer import PersonSerializer

from persons.models import Person
class CreatePerson(views.APIView):
    """
    End point to add Persons
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        serializer = PersonSerializer(data=request.data)
         if serializer.is_valid():
            serializer.save()
            return response.Response(
                serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def pre_save(self, obj):
        obj.created_by = self.request.user


class GetPersonsByUser(views.APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        user = request.user
        queryset = Person.objects.filter(created_by = user)
        

