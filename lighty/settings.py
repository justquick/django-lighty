from django.conf import settings

FCGI = getattr(settings, 'LIGHTY_FCGI', 'method=prefork minspare=2 maxspare=4 maxchildren=5')
USER = getattr(settings, 'LIGHTY_USER', 'lighttpd')

HOSTS = getattr(settings, 'LIGHTY_HOSTS', {})



