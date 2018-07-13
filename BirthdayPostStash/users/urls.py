from django.conf.urls import url
from . import apis

urlpatterns = [
    url(r'register/$', apis.UserRegister.as_view(), name='api_user_register')
]
