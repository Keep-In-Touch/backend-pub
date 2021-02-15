from django.contrib import admin

from .models import *


# Register your models here.
class FCMTokenAdmin(admin.ModelAdmin):
    search_fields = ('user', 'token')


admin.site.register(FCMToken, FCMTokenAdmin)
