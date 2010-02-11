import os,sys
from fabric.api import *
from fabric import api
from fabric.contrib.project import rsync_project
from fabric.contrib.files import append
from fabric.contrib.files import exists

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings as django_settings
from django.db.models import get_model
from lighty.models import Site, Server, Django
from lighty import settings
from lighty.util import *
from getpass import getuser

def ps():
    run('ps -C python -o pid,command')

def err():
    sudo('tail -50 /var/log/lighttpd/error.log')

def cnf():
    run('tail -100 /etc/lighttpd/lighttpd.conf')

        

#class Application:
#    host
#    port
#    url
#    
#class Server:
#    name
#    virtualenv_name
#    user
#    address
#    port

def run(*a,**kw):
    return api.run(*a,**kw)
    
def sudo(*a,**kw):
    return api.sudo(*a,**kw)
    
def put(*a,**kw):
    return api.put(*a,**kw)
    
def killall(p):
    run('killall %s'%p)

def service(name,action='status'):
    sudo('/etc/init.d/%s %s' % (name,action))

def lighty(action='status'):
    service('lighty',action)
        

deploy = Server.objects.get(pk=1)
active = None
env.hosts = [deploy.address]
env.user = deploy.user

def host(name):
    global env,active
    if name == 'all':
        env.hosts = [s.address for s in Server.objects.active()]
    else:
        active = Server.objects.active(name=name)[0]
        env.user = active.user
        env.hosts = [active.address]

hosts = lambda: host('all')

def rollout():
    global active,env
    active = deploy
    init()
    perms()
    sync()
    conf()
    restart()
    for server in Server.objects.active(pk__lt=deploy.pk)|Server.objects.active(pk__gt=deploy.pk):
        if env.host == server.address:
            active = server
            install()
            break

def workon(cmd):
    return run('workon %s; %s' % (deploy.name, cmd))

def sysinit():
    sharekey()    
    sudo('apt-get -y install gcc lighttpd python python-dev python-setuptools')
    sudo('easy_install virtualenv==1.3.4 virtualenvwrapper==1.20 flup==1.0.2 fabric==0.9.0')
    run('echo "source /usr/local/bin/virtualenvwrapper_bashrc" >> ~/.profile')
        
def init():
    global env
    venvs = '/' + os.path.join('home', env.user , '.virtualenvs')
    if not exists(venvs):
        run('mkdir %s' % venvs)
    if not exists(settings.ROOT):
        sudo('mkdir %s' % settings.ROOT)
        sudo('chown -R %s %s' % (env.user,settings.ROOT))

    name = os.path.join(settings.ROOT, active.name)
    if not exists(name):
        run('mkdir %s' % name)
            #                  ';'.join([
            #'cp %s %s' % (os.path.join(settings.ROOT, active.name, 'site_template', f), name) \
            #for f in ('__init__.py','settings.py','manage.py','urls.py','requirements.txt')] )))
    if not os.path.isdir(name):
        local('mkdir %s' % name)        

def sync():
    global env
    for name in (deploy.name,active.name):
        rsync_project(remote_dir=os.path.join(settings.ROOT,name),
            local_dir=os.path.join(settings.ROOT, name)+'/')
        
def mkvenv():
    global env
    venvs = '/' + os.path.join('home', env.user , '.virtualenvs')
    if not exists(os.path.join(venvs,active.name)):
        run('mkvirtualenv %s' % active.name)
    if not exists(os.path.join(venvs,deploy.name)):
        run('mkvirtualenv %s' % deploy.name)
    workon('easy_install pip')
    
def requirements():
    reqs = os.path.join(settings.ROOT, active.name,'requirements.txt')
    if exists(reqs):
        workon('cd %s; pip install -r requirements.txt' % os.path.join(settings.ROOT,active.name))
    
def perms():
    global env
    for name in (deploy.name,active.name):
        dbfile = os.path.join(settings.ROOT, name, os.path.basename(django_settings.DATABASE_NAME))
        p = os.path.join(settings.ROOT, name)
        if not exists(p):
            run('mkdir %s'%p)
        if not exists(dbfile):
            run('touch %s' % dbfile)
        sudo('chown %s:%s %s' % (env.user, settings.USER, dbfile))
        sudo('chmod 770 %s' % dbfile)
    
def manage(*args):
    name = active.name
    if len(args) and args[0] == 'lightyctl':
        name = deploy.name
    workon('python %s %s' % (os.path.join(settings.ROOT,name,'manage.py'), ' '.join(args)))
    
def conf():
    conf = os.path.join(settings.ROOT, active.name,'lighttpd.conf')
    manage('lightyctl', 'configure', active.name, '>', conf)
    sudo('cp %s %s' % (conf, settings.CONF))

def stop():
    pidfile = lambda name: os.path.join(settings.ROOT, name, '.pid')
    kill = lambda pid: run('kill `cat %s`; rm -f %s' % (pid,pid))
    if active:
        kill(pidfile(active.name))
    else:
        for server in Server.objects.active():
            kill(pidfile(server.name))
        
def start():
    global active
    for server in Server.objects.active(pk__lt=deploy.pk)|Server.objects.active(pk__gt=deploy.pk):
        if env.host != server.address or not exists(os.path.join(settings.ROOT, server.name)): continue    
        for app in Django.objects.filter(host=server):
            active = server
            pidfile = os.path.join(settings.ROOT, server.name, '.pid')
            manage(*['runfcgi','pidfile=%s' % pidfile] + app.fcgi())

def restart():
    stop(); start()
    
def reset():
    sudo('rm -rf /var/code')
    killall('python')
    
def push():
    global active
    for server in Server.objects.active(pk__lt=deploy.pk)|Server.objects.active(pk__gt=deploy.pk):
        if env.host != server.address: continue
        active = server
        sync()
        conf()
        restart()
        perms()
        lighty('force-reload')
    
def sharekey(pub='~/.ssh/id_rsa.pub'):
    """ssh-keygen -t rsa -b 1024"""
    global env
    ssh = '/' + os.path.join('home', env.user, '.ssh')
    if not exists(ssh):
        run('mkdir %s' % ssh)
    xpub = os.path.join(ssh, 'authorized_keys')
    if exists(xpub):
        run('chmod +w %s' % xpub)
    put(os.path.expanduser(pub), xpub)
    run('chmod 400 %s' % xpub)

def install():
    init() # setup packages/base directory
    perms()
    sync() # rsync deploy project
    mkvenv() # mkvirtualenv and add pip
    requirements() # install project requirements
    conf() # affix lighttpd.conf
    restart() # restart fastcgi handlers
    perms()
    lighty('restart') # restart lighttpd

