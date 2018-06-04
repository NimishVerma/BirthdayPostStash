from django.conf.urls import url
from . import views
from django.contrib.auth.views import login,logout
#from BirthdayPostStash import views as Bpsviews

urlpatterns = [
    url(r'login/$', login, {'template_name':'login.html'}),
    url(r'logout/$', logout, {'template_name':'logout.html'}),
    url(r'register/$', views.register,name='register'),	
    url(r'profile/$', views.profile, name='profile'),
    url(r'^$', views.login_redirect ),



    
]
