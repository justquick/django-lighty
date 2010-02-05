#!{{ exe }}
import sys, os

# Add a custom Python path.
sys.path.insert(0, "{{ document_root }}")

os.chdir("{{ document_root }}")

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")

