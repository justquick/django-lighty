from django.conf import settings

FCGI = getattr(settings, 'LIGHTY_FCGI', 'method=prefork minspare=2 maxspare=4 maxchildren=5')
USER = getattr(settings, 'LIGHTY_USER', 'lighttpd')
ROOT = getattr(settings, 'LIGHTY_ROOT', '/var/code')
PIDFILE = getattr(settings, 'LIGHTY_PIDFILE', '.pid')
SOCKFILE = getattr(settings, 'LIGHTY_SOCKFILE', '.sock')
CONF = getattr(settings, 'LIGHTY_CONF', '/etc/lighttpd/lighttpd.conf')