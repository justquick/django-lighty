.. _management:
.. highlight:: django

Management
==============

Administrating Sites
---------------------

Out of the box, Lighty comes with its own ``deploy`` project which provides access to the site structure using the django admin.

Create a normal ``Site``
^^^^^^^^^^^^^^^^^^^^^^^^^

Create a ``ProxySite``
^^^^^^^^^^^^^^^^^^^^^^^^^


Lighttpd Config Dump
----------------------

Lighttpd configuration is created using the ``lightyctl`` management command and is harnessed by Lighttpd using the ``include_shell`` directive to import them on the fly.

Some common examples are

With VirtualEnv (recomended)::

    include_shell "/home/$USER/.virtualenvs/deploy/bin/python /var/code/deploy/manage.py lightyctl"

Without::
    
    include_shell "/var/code/deploy/manage.py lightyctl"
    
Deploying Sites
----------------

Fabric magic




