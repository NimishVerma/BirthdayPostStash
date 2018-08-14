from django.conf.urls import url
from . import apis

urlpatterns = [
    url(r'register/$', apis.UserRegister.as_view(), name='api_user_register'),
    url(r'login/$', apis.UserLogin.as_view(), name='api_user_login'),
    url(r'logout/$', apis.UserLogout.as_view(), name='api_user_logout'),
    url(r'token/$', apis.GetToken.as_view(), name='api_user_token'),
    url(
        r'setup-profile/$',
        apis.SetupUserProfile.as_view(),
        name='api_setup_profile'
    ),
    url(
        r'profile/(?P<username>[0-z]+)$',
        apis.GetUserProfile.as_view(),
        name='api_get_profile'
    )
]
