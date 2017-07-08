from django.contrib import admin
from staff.models import Member, History, Schedule
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin


# user = User.objects.create_user(Profile.name, Profile.email, Profile.password)

class CustomUserAdmin(UserAdmin):
    def __init__(self, *args, **kwargs):
        super(UserAdmin, self).__init__(*args, **kwargs)
        UserAdmin.list_display = list(UserAdmin.list_display) #default값

        def username(self, obj):
            print ("%s" % (obj.username))
        username(self, User)

    # def get_total(request):
    #     members = request.user.members.all()
    #     for member in members:
    #         print(member)
    # get_total(User)

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


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
# admin.site.register(Member)