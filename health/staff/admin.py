from django.contrib import admin
from staff.models import Member, History, Schedule
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin


class HistoryInline(admin.TabularInline):
    model = History

class ScheduleInline(admin.TabularInline):
    model = Schedule

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','birth','sex']
    search_fields = ['name']
    inlines = [
        HistoryInline,
        ScheduleInline,
    ]

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ['id','user','birth']
    search_fields = ['user']

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['Trainer','title','start']
    search_fields = ['title','start']


# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)
# admin.site.register(Member)