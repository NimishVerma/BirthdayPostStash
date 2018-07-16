from django.utils.deprecation import MiddlewareMixin


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
            request.META['HTTP_AUTHORIZATION'] = auth_cookie

        return None
