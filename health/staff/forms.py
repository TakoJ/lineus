from django import forms
from .models import Member, PaymentHistory, History, Schedule
from functools import partial

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('division','name','birth','phone_num','address','sex','registered_date', 'start_date', 'end_date', 'type_choice','rating','period_fitness','period_pilates','period_both', 'locker','period_locker','cautions','exercise_time','visit_path','membership_amount','locker_amount','payment_amount','payment_method','note')

# class PaymentHistoryForm(forms.ModelForm):
#     class Meta:
#         model = PaymentHistory
#         fields = ()



class PT_RegisterForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('registered_session','PT_payment_amount','PT_payment_method','unitprice','period_PT')

class PT_Register_HistoryForm(forms.ModelForm):
    class Meta:
        model = History
        fields = ('registered_session','PT_payment_amount','PT_payment_method','unitprice','period_PT')

class Schedule_AddForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ('title','start','end','Trainer')

class DateRangeForm(forms.Form):
    DateInput = partial(forms.DateInput, {'class': 'datepicker'})

    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())