from django.db import models
from django.contrib.sites.models import Site as DjangoSite
from django.template.loader import render_to_string


WWW = (
    (0, 'Take out www.'),
    (1, 'Both work'),
    (2, 'Only www.'),
)


class Alias(models.Model):
    url = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    
    def __unicode__(self):
        return u'%s => %s' % (self.url, self.path)
        
class Rewrite(models.Model):
    regex = models.CharField(max_length=255)
    uri = models.CharField(max_length=255)
    
    def __unicode__(self):
        return u'%s => %s' % (self.regex, self.uri)

class LightySite(models.Model):
    site = models.ForeignKey(DjangoSite)
    document_root = models.CharField(max_length=255,blank=True,null=True)
    dir_listing = models.BooleanField(default=False)
    follow_symlink = models.BooleanField(default=True)
    www = models.IntegerField('WWW',default=1,choices=WWW)
    
    aliases = models.ManyToManyField(Alias,blank=True,null=True)
    rewrites = models.ManyToManyField(Rewrite,blank=True,null=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return unicode(self.site)
    
    def name(self):
        return self.site.name
    name = property(name)
    
    def hostescape(self):
        return self.site.domain.replace('.','\\.').replace('-','\\-').replace('_','\\_')
    hostescape = property(hostescape)
    
    def save(self, *a, **kw):
        if not self.document_root:
            self.document_root = '/var/code/%s' % self.site.name
        super(LightySite, self).save(*a, **kw)

    def render(self):
        return render_to_string(self.get_template(), {'site':self})


class Site(LightySite):
    def get_template(self):
        return 'lighty/hosts.conf'


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
    backends = models.ManyToManyField(Site,related_name='proxy_backends')
    max_pool_size = models.PositiveIntegerField(default=5)
    allow_x_sendfile = models.BooleanField(default=False)
    allow_x_rewrite = models.BooleanField(default=False)
    balancer = models.IntegerField(default=2,choices=BALANCER)
    
    def get_template(self):
        return 'lighty/proxies.conf'