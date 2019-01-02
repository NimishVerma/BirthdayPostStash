
from __future__ import unicode_literals

from django.conf.urls import url

from .apis import *


urlpatterns = [
    url(r'^add-friend/',
        CreatePerson.as_view(),
        name="api_create_person"),
    url(r'^list-friend/',
        GetPersonsByUser.as_view(),
        name="api_list_persons_by_user"),
    url(r'^get-top-five/',
	GetTopFive.as_view(),
	name="api_get_top_five"),
]

