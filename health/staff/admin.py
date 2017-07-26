from django.contrib import admin
from staff.models import Member, MembershipHistory, History, Pil_History, Schedule, PaymentHistory, RefundHistory
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
    list_display = ['id', 'name','birth','sex', 'registered_date']
    search_fields = ['name']
    inlines = [
        HistoryInline,
        ScheduleInline,
    ]

@admin.register(MembershipHistory)
class MembershipHistoryAdmin(admin.ModelAdmin):
    list_display = ['user','birth','registered_date','start_date','end_date']

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ['id','user','birth']
    search_fields = ['user']

@admin.register(Pil_History)
class Pil_HistoryAdmin(admin.ModelAdmin):
    list_display = ['id','user','birth']
    search_fields = ['user']

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['Trainer','title','start']
    search_fields = ['title','start']

@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ['user','uid','division','date','end_date','payment_amount']

@admin.register(RefundHistory)
class RefundHistoryAdmin(admin.ModelAdmin):
    list_display = ['payment','refund_date','refund_amount']


# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)
# admin.site.register(Member)