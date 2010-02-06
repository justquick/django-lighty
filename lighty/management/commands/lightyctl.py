from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from lighty import settings
from lighty.models import Site, ProxySite
from lighty.util import *
from subprocess import call, check_call
import os

        
class Command(BaseCommand):
    def handle(self, *args, **options):
        if len(args):
            if '_'+args[0] in dir(self):
		getattr(self, '_'+args[0])(*args[1:])
	    else:
		raise CommandError('Command "%s" not found' % args[0])
        else:            
            exe = vpath('deploy','python')
            manage = os.path.join(settings.ROOT, 'deploy', 'manage.py')
            print 'include_shell "%s %s lightyctl configure"\n' % (exe, manage)
    
    def _stop(self, *args):
        for name in args:
            _,_cmds = cmds(name)
            _,pidfile,_ = get_files(name)
            if os.path.isfile(pidfile):
                call(_cmds + ['kill', open(pidfile).read().strip()])
                call(_cmds + ['rm', '-f', pidfile])
            
    def _start(self, *args):
        for name in args:
            proj_dir, pidfile, sockfile = get_files(name)
            if not os.path.isfile(sockfile): 
                check_call(['touch', sockfile])            
                check_call(['sudo', 'chown', settings.USER, sockfile])
            # $ python ./manage.py runfcgi [options...]
            os.system(' '.join(cmds(name) + [vpath(name, 'python'),
                    os.path.join(proj_dir, 'manage.py'), 'runfcgi', 
                    'pidfile=%r' % pidfile, 'socket=%r' % sockfile] + \
                    settings.FCGI.split()))
        
    def _restart(self, *args):
        for name in args:
            self.stop(name)
            self.start(name)
            
    def _deploy(self, *args):
	fab = vpath('deploy','fab')
	if not len(args):
	    args = ('deploy',)
        for name in args:
            call((fab, 'deploy:name=%s' % name))
            
    def _configure(self, *args):
	if len(args):
	    for arg in args:
		for model in (Site, ProxySite):
		    try:
			print model.objects.get(name=arg).render()
		    except model.DoesNotExist:
			continue
	else:
	    for model in (Site, ProxySite):
		for site in model.objects.all():
		    print site.render()

    def _fab(self, *args):
	call(('fab',) + args)



