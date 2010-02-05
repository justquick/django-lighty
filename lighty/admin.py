from django.contrib import admin
from models import Site, ProxySite, Alias, Rewrite


class SiteAdmin(admin.ModelAdmin):
    raw_id_fields = ('site',)
    
admin.site.register(Site, SiteAdmin)
admin.site.register(ProxySite, SiteAdmin)
admin.site.register(Alias)
admin.site.register(Rewrite)
