from django.contrib import admin

# Register your models here.

from .models import *

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Member"
        verbose_name_plural = "Members"

admin.site.register(Menu)
admin.site.register(Item)
admin.site.register(Option)
admin.site.register(Order)