from django.contrib import admin
from .models import ClockIn, SetUp, Balance

# Register your models here.


@admin.register(ClockIn, SetUp, Balance)
class GoalAdmin(admin.ModelAdmin):
    pass
