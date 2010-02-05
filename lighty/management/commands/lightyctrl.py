from django.core.management.base import BaseCommand
from lighty import settings
from django.template.loader import render_to_string
from subprocess import check_call
import os,sys

def get_files(name):
    d = os.path.join("/var/code/", arg)
    return d, os.path.join(proj_dir, '.pid'), os.path.join(proj_dir, '.sock')
    
class Command(BaseCommand):
    def handle(self, *args, **options):
	if len(args) and args[0] == 'configure':
	    for name,data in settings.HOSTS.items():
		proj_dir, pidfile, sockfile = get_files(name)
		data.update({
		    'hostescape': data['host'].replace('.','\\.').replace('-','\\-').replace('_','\\_'),
		    'name': name,
		    'document_root': proj_dir,
		    'sockfile': sockfile,
		    'base': '/var/code',
		    'no_www': data.get('www',1) == 0,
		    'force_www': data.get('www',1) == 1,
		    'follow_symlink': data.get('follow_symlink', True)
		})
		print render_to_string('light/hosts.conf', data)
		
	elif len(args):
	    for name in args:
		if not name in settings.HOSTS: continue
		proj_dir, pidfile, sockfile = get_files(name)
		
		venv = True
		exe = os.path.expanduser('~/.virtualenvs/%s/bin/python' % name)
		cmds = []
		if not os.path.isfile(exe):
		    exe = sys.executable
		    venv = False
		    cmds = ['sudo', '-u', settings.USER]

		if os.path.isfile(pidfile):
		    check_call(cmds + ['kill', open(pidfile).read().strip()])
		    check_call(cmds + ['rm', '-f', pidfile])
		os.chdir(proj_dir)

		    
		check_call(cmds + [exe, os.path.join(dir, 'manage.py'), 'runfcgi', 
			'pidfile=%r' % pidfile, 'socket=%r' % sockfile] +
			settings.FCGI.split())
		check_call(['sudo', 'chown', settings.USER, sockfile])
