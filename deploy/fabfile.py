from fabric.api import *
from fabric.contrib.project import rsync_project
import os,sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.db.models import get_model
from lighty.models import Site, ProxySite
from lighty import settings
from lighty.util import *
from getpass import getuser

address = lambda s: s.address
sites = tuple(Site.objects.filter(active=True)) + tuple(ProxySite.objects.filter(active=True))
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

def restart(name='deploy'):
    for site in itr(name):
        run('workon %s; %s/%s/manage.py lightyctl %s' % (name, settings.ROOT, name, name))
        
def install():
    try:
        sudo('mkdir %s' % settings.ROOT)
        sudo('chown -R %s %s' % (env.user,settings.ROOT))
    except:
        pass
    try:
        run('cd %s; git clone http://github.com/justquick/django-lighty.git' % settings.ROOT)
    except:
        run('cd %s/django-lighty; git pull origin master' % settings.ROOT)
    rsync_project(remote_dir=settings.ROOT, local_dir=os.path.join(settings.ROOT, 'deploy'))
    run('mkvirtualenv deploy')
    run('workon deploy; pip install -r %s/deploy/requirements.txt' % settings.ROOT)
    sudo('cd %s; cp deploy/lighttpd.conf.sample %s' % (settings.ROOT,settings.CONF))
    run('workon deploy; %s/deploy/manage.py syncdb --noinput' % settings.ROOT)
    run('workon deploy; %s/deploy/manage.py loaddata *.json' % settings.ROOT)
    sudo('workon deploy; %s/deploy/manage.py lightyctl >> %s' % (settings.ROOT, settings.CONF))
    sudo('/etc/init.d/lighttpd restart')
        
def lighty(name=None,action='status'):
    for site in itr(name):
        sudo('/etc/init.d/lighttpd %s' % action)