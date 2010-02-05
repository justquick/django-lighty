.. _configuration:
.. highlight:: python

Install
========

Tested to work with Ubuntu linux, though other distiributions like Debian,CentOS,Fedora have also been proven to work.
In the following configuration setup, replace ``$USER`` with your username if you are running VirtualEnv, otherwise lighttpd's running username.

Install Lighty/FastCGI
-------------------------

Django-Lighty requires Lighttpd>=1.4.22, Django==1.1.1, flup==1.0.2.

::

    sudo apt-get -y install lighttpd
    sudo apt-get build-dep lighttpd
    sudo lighttpd-enable-mod fastcgi
    sudo /etc/init.d/lighttpd force-reload

With VirtualEnv (recomended)::
    
    mkvirtualenv deploy
    easy_install -U flup==1.0.2 django==1.1.1 

Without::
    
    sudo easy_install -U flup==1.0.2 django==1.1.1 

Install the ``deploy`` project
--------------------------------

This is the main project for managing your sites, restarting fcgi handlers, lighttpd configuration and more

::

    sudo mkdir /var/code
    cd /var/code
    sudo chown -R $USER .
    git clone http://github.com/justquick/django-lighty.git
    mv django-lighty/deploy .
    mv django-lighty/lighty deploy
    # Use the example config, or edit your own below
    # sudo mv django-lighty/lighttpd.conf.sample /etc/lighttpd/lighttpd.conf
    cd deploy
    ./manage.py syncdb
    ./manage.py loaddata *.json
    
Configure Lighttpd
-------------------

Edit your Lighttpd configuration file ususally located in  ``/etc/lighttpd/lighttpd.conf``. A sample Debian configuration file is available at ``lighttpd.conf.sample``. 
Adjust your ``server.modules`` to contain the following::

    server.modules = (
        "mod_access",
        "mod_alias",
        "mod_accesslog",
        "mod_compress",
        "mod_rewrite",
        "mod_redirect",
        "mod_fastcgi",
    )
    

Add deploy configuration at the last line

With VirtualEnv (recomended)::

    include_shell "/home/$USER/.virtualenvs/deploy/bin/python /var/code/deploy/manage.py lightyctl"

Without::
    
    include_shell "/var/code/deploy/manage.py lightyctl"