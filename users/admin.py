from django.contrib import admin

from .models import *
# TODO add users

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name', 'email')


admin.site.register(User, UserAdmin)
