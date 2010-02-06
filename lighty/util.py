import os
import sys
import settings

def get_files(name):
    d = os.path.join(settings.ROOT, name)
    return d, os.path.join(d, settings.PIDFILE), os.path.join(d, settings.SOCKFILE)

def cmds(name):
    return vpath(name,'python') == sys.executable and ['sudo', '-u', settings.USER] or []
    
def vpath(name,bin):
    exe = os.path.expanduser('~/.virtualenvs/%s/bin/%s' % (name, bin))
    if not os.path.isfile(exe):
        if bin == 'python':
            return sys.executable
        return bin
    return exe
