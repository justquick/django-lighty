Django-Lighttpd Documentation
==============================

:Authors:
   Justin Quick <justquick@gmail.com>
:Version: 0.1

Django-Lighty is able to deploy multiple `Django <http://www.djangoproject.org/>`_ sites using `Lighttpd <http://lighttpd.net>`_ and `FastCGI <http://www.fastcgi.com/>`_ in production. 
It generates the configuration and manages the FastCGI processes with the ability to reload them independently. 
Sites are defined in the db and can be rolled out using a few management commands.
Supports proxying among multiple backends for load balancing.
Provides `Fabric <http://docs.fabfile.org/0.9.0/>`_ deployment files for pushing out projects to multiple servers.
It plays nicely with `VirtualEnv <http://virtualenv.openplans.org/>`_ based projects.


TODO
=======

* Add Fab deploy script
* Test proxying/clustering