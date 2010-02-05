from django.conf import settings

FCGI = getattr(settings, 'LIGHTY_FCGI', 'method=prefork minspare=2 maxspare=4 maxchildren=5')
USER = getattr(settings, 'LIGHTY_USER', 'lighttpd')

HOSTS = getattr(settings, 'LIGHTY_HOSTS', {})

{
    'trydjango':{
        'www': 0,
        'host': 'trydjango.com',
        'aliases': (
            ('/site_media', 'site_media'),
        ),
        'rewrites': (
            ("^(/site\_media.*)$", "$1"),
        )
    },
    'ec':{
        'www':0,
        'host':'effervescentcollective.kicks-ass.org',
        'aliases': (
            ('/media', 'media'),
        ),
        'rewrites': (
            ("^(/media.*)$", "$1"),
        ),        
    }
}


