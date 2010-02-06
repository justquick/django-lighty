from fabric.api import *
import os,sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.db.models import get_model
from lighty.models import Site, ProxySite
from lighty import settings
from lighty.util import *
from getpass import getuser

address = lambda s: s.address
sites = tuple(Site.objects.all()) + tuple(ProxySite.objects.all())
env.hosts = map(address, sites)

def setup(site):
    env.hosts = [site.address]
    env.user = site.user
    
def workon(name):
    run('workon %s')
    
def itr(name=None):
    for site in sites:
        if name and site.name != name:
            continue
        if site.address == env.host:    
            setup(site)
            yield site

def deploy(name='deploy'):
    for site in itr(name):
        run('whoami')
        
def install(name='deploy'):
    sudo('mkdir %s' % settings.ROOT)
    sudo('chown -R %s %s' % (env.user,settings.ROOT))
    run('cd %s; git clone http://github.com/justquick/django-lighty.git' % settings.ROOT)
    run('cd %s; mv django-lighty/deploy .' % settings.ROOT)
    run('cd %s; rm -r django-lighty' % settings.ROOT)
    sudo('cd %s; cp deploy/lighttpd.conf.sample %s' % (settings.ROOT,settings.CONF))
    run('mkvirtualenv deploy')
    run('workon %s; easy_install -U pip flup==1.0.2 django==1.1.1 fabric==0.9.0' % name)
    run('workon %s; pip install git+http://github.com/justquick/django-lighty.git' % name)
    run('workon %s; %s/%s/manage.py syncdb' % (name, settings.ROOT, name))
    run('workon %s; %s/%s/manage.py loaddata *.json' % (name, settings.ROOT, name))
    run('workon %s; %s/%s/manage.py lightyctl >> %s' % (name, settings.ROOT, name, settings.CONF))
        
def lighty(name=None,action='status'):
    for site in itr(name):
        sudo('/etc/init.d/lighttpd %s' % action)