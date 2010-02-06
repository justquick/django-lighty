import os
import sys
import settings

def get_files(name):
    d = os.path.join(settings.ROOT, name)
    return d, os.path.join(d, settings.PIDFILE), os.path.join(d, settings.SOCKFILE)

def exe(name='deploy'):
    exe = vpath(name)
    return os.path.isfile(exe) and exe or sys.executable

def cmds(name):
    return exe(name) == sys.executable and ['sudo', '-u', settings.USER] or []
    
def vpath(name,bin):
    exe = os.path.expanduser('~/.virtualenvs/%s/bin/%s' % (name, bin))
    if not os.path.isfile(exe):
        if bin == 'python':
            return sys.executable
        return bin
    return exe
