  
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from . import models

class UrlAdmin(admin.ModelAdmin):
    list_display = ('slug', 'target', 'created_on')
    search_fields = ('slug', 'target', 'created_on')
    list_filter = ('slug', 'target', 'created_on')

class ClickAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    list_display = ('url', 'client_ip', 'referer', 'user_agent')
    search_fields = ('url', 'client_ip', 'referer', 'user_agent')
    list_filter = ('url', 'client_ip', 'referer', 'user_agent')


admin.site.unregister(Group)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Url, UrlAdmin)
admin.site.register(models.Click, ClickAdmin)

