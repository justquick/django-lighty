from django.db import models
from django.contrib.sites.models import SiteManager
from django.template.loader import render_to_string
from getpass import getuser
from django.conf import settings as django_settings
import settings
import os

WWW = (
    (0, 'Take out www.'),
    (1, 'Both work'),
    (2, 'Only www.'),
)

class Module(models.Model):
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.name

class Alias(models.Model):
    url = models.CharField('URL-subset',max_length=255)
    path = models.CharField('document root',max_length=255)
    
    def __unicode__(self):
        return u'%s => %s' % (self.url, self.path)
        
    class Meta:
        verbose_name_plural = 'Aliases'
        
class Rewrite(models.Model):
    regex = models.CharField(max_length=255)
    uri = models.CharField(max_length=255)
    
    def __unicode__(self):
        return u'%s => %s' % (self.regex, self.uri)

class LightySite(models.Model):
    name = models.CharField('display name', max_length=50)
    domain = models.CharField('binding domain', max_length=100)
    address = models.IPAddressField('internal server address', max_length=100, unique=True)
    user = models.CharField('SSH username', max_length=255, default=getuser())
    port = models.PositiveIntegerField('listening port',default=80)
    document_root = models.CharField(max_length=255,blank=True,null=True)
    follow_symlink = models.BooleanField(default=True)
    www = models.IntegerField('WWW',default=1,choices=WWW)
    repo = models.CharField('repository url',max_length=255,null=True,blank=True)
    
    max_keep_alive_requests = models.IntegerField(default=16)
    max_keep_alive_idle = models.IntegerField(default=5)
    max_read_idle = models.IntegerField(default=60)
    max_write_idle = models.IntegerField(default=360)
    
    aliases = models.ManyToManyField(Alias,blank=True,null=True)
    rewrites = models.ManyToManyField(Rewrite,blank=True,null=True)
    modules = models.ManyToManyField(Module,blank=True,null=True)
    
    objects = SiteManager()
    
    @property
    def template(self):
        return

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name
        
    def hostescape(self):
        return self.domain.replace('.','\\.').replace('-','\\-').replace('_','\\_')
    hostescape = property(hostescape)
    
    def save(self, *a, **kw):
        if not self.document_root:
            self.document_root = os.path.join(settings.ROOT, self.name)
            
        super(LightySite, self).save(*a, **kw)

        if not self.aliases.count():
            self.aliases.add(Alias.objects.create(
                url=django_settings.MEDIA_URL,
                path=django_settings.MEDIA_ROOT))
            self.rewrites.add(Rewrite.objects.create(
                regex=r'^(%s.*)$' % django_settings.MEDIA_URL,
                uri='$1'
            ))
            
        if not self.modules.count():
            map(lambda n: self.modules.add(Module.objects.create(name=n)),[
                    "mod_access",
                    "mod_alias",
                    "mod_accesslog",
                    "mod_compress",
                    "mod_rewrite",
                    "mod_redirect",
                    "mod_fastcgi"])


    def render(self):
        return render_to_string(self.template or 'lighty/hosts.conf', {'site':self})

class Site(LightySite):
    pass


BALANCER = (
    (0, 'round-robin'),
    (1, 'sqf'),
    (2, 'carp'),
    (3, 'static'),
)


class ProxySite(LightySite):
    #"10.0.0.1:80",     ## IPv4 address
    #"unix:/tmp/php.socket", ## unix domain socket
    #"[::1]:80",        ## IPv6 addresss
    #"google.com:80"    ## hostname, resolved at startup
    backends = models.CharField(max_length=255)
    max_pool_size = models.PositiveIntegerField(default=5)
    allow_x_sendfile = models.BooleanField(default=False)
    allow_x_rewrite = models.BooleanField(default=False)
    balancer = models.IntegerField(default=2,choices=BALANCER)
    
    @property
    def template(self):
        return 'lighty/proxies.conf'
    
    def get_backends(self):
        if self.backends.find(',')>-1:
            return self.backends.split(',')
        return self.backends.split()

if not Module.objects.count():
    map(lambda n: Module.objects.create(name=n),[
        "mod_evhost",
        "mod_usertrack",
        "mod_rrdtool",
        "mod_webdav",
        "mod_expire",
        "mod_flv_streaming",
        "mod_evasive"])
    
if not Site.objects.count():
    Site.objects.create(
        name='deploy',
        domain='localhost',
        address='127.0.0.1',
        www=0,
    )
    
