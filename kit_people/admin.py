from django.contrib import admin

from .models import *


# Register your models here.
class RoleAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class RegularityAdmin(admin.ModelAdmin):
    search_fields = ('notification_type', 'kit_person')

class KitPersonAdmin(admin.ModelAdmin):
    search_fields = ('name', 'priority', 'contact')


class InteractionAdmin(admin.ModelAdmin):
    search_fields = ('date', 'interaction_way')


admin.site.register(Role, RoleAdmin)
admin.site.register(KitPerson, KitPersonAdmin)
admin.site.register(Interaction, InteractionAdmin)
admin.site.register(Regularity, RegularityAdmin)
