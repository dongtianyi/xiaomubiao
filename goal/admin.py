from django.contrib import admin
from .models import ClockIn, SetUp, Balance

# Register your models here.


class SetUpAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'status', 'created_time')


class ClockInAdmin(admin.ModelAdmin):
    list_display = ('user', 'setup', 'image_0', 'created_time')


class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'created_time')


admin.site.register(SetUp, SetUpAdmin)
admin.site.register(ClockIn, ClockInAdmin)
admin.site.register(Balance, BalanceAdmin)
