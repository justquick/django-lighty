.. _configuration:
.. highlight:: python

Settings
========

LIGHTY_FCGI
-------------------

String arguments to pass ``./manage.py runfcgi``. Default: ``method=prefork minspare=2 maxspare=4 maxchildren=5``


LIGHTY_USER
-------------------

Either your username if you are running VirtualEnv, otherwise lighttpd's running username. Default: ``lighttpd``


