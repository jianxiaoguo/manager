from django.contrib import admin
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from api.models import Cluster


class ClusterAdmin(admin.ModelAdmin):
    list_display = ('name', 'ingress',)
    search_fields = ('name',)


admin.site.site_header = 'Workflow Manager'
admin.site.site_title = 'Workflow Manager'
admin.site.register(Cluster, ClusterAdmin)

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(Token)
