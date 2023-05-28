from django.contrib import admin
from .models import *

class LoginRDBMS(admin.ModelAdmin):
    list_display = ('id', 'ip_address', 'username', 'password1', 'password2', 'date', 'update_date')


class BlackListRDBMS(admin.ModelAdmin):
    list_display = ('id', 'username', 'date', 'update_date')






admin.site.register(Logins, LoginRDBMS)
admin.site.register(Blacklist,BlackListRDBMS)

