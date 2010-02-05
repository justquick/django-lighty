from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from lighty import settings
from lighty.models import Site, ProxySite
from subprocess import call, check_call
import os,sys

def get_files(name):
    d = os.path.join('/var/code/', name)
    return d, os.path.join(d, '.pid'), os.path.join(d, '.sock')
    
class Command(BaseCommand):
    def handle(self, *args, **options):
	if len(args):
	    for name in args:
		if not name in os.listdir('/var/code'): continue
		proj_dir, pidfile, sockfile = get_files(name)
		
		exe = os.path.expanduser('~/.virtualenvs/%s/bin/python' % name)
		cmds = []
		if not os.path.isfile(exe):
		    exe = sys.executable
		    cmds = ['sudo', '-u', settings.USER]

		if os.path.isfile(pidfile):
		    call(cmds + ['kill', open(pidfile).read().strip()])
		    call(cmds + ['rm', '-f', pidfile])
		os.chdir(proj_dir)
		cmds = cmds + [exe, os.path.join(proj_dir, 'manage.py'), 'runfcgi', 
			'pidfile=%r' % pidfile, 'socket=%r' % sockfile] + \
			settings.FCGI.split()
                os.system(' '.join(cmds))
		while 1:
                    if os.path.isfile(sockfile): 
                        check_call(['sudo', 'chown', settings.USER, sockfile])
                        break
	else:	    
	    for site in Site.objects.all():
		print site.render()
	    for site in ProxySite.objects.all():
		print site.render()
		
