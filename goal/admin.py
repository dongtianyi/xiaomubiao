from django.contrib import admin
from .models import ClockIn, SetUp, Balance

# Register your models here.


class SetUpAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'status')


class ClockInAdmin(admin.ModelAdmin):
    list_display = ('user', 'setup', 'image_0')


class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'created_time')


admin.site.register(SetUp, SetUpAdmin)
admin.site.register(ClockIn, ClockInAdmin)
admin.site.register(Balance, BalanceAdmin)
