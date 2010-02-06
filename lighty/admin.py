from django.contrib import admin
from models import Site, ProxySite, Alias, Rewrite, Module


    
map(admin.site.register, (Site,ProxySite,Alias,Rewrite,Module))