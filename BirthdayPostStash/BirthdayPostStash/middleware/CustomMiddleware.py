import pytz
import datetime
from django.utils.deprecation import MiddlewareMixin
from rest_framework.authtoken.models import Token


class CustomMiddleware(MiddlewareMixin):

    '''
    Custom Middleware to edit request for swagger mainly
    - takes authtoken from COOKIES
    and sets that as Authorization header
    '''

    def process_request(self, request):
        auth_cookie = request.META.get('HTTP_AUTHORIZATION')
        if auth_cookie:
            return None
        auth_cookie = request.COOKIES.get('Authorization')
        if auth_cookie:
            token = auth_cookie.replace('Token ', '')
            try:
                token_obj = Token.objects.get(key=token)
            except:
                token_obj = None
            if token_obj:
                now = pytz.UTC.localize(datetime.datetime.now())
                token_expiry_time = token_obj.created + datetime.timedelta(
                    minutes=30)
                if now < token_expiry_time:
                    token_obj.created = now
                    token_obj.save()
                    request.META['HTTP_AUTHORIZATION'] = auth_cookie

        return None
