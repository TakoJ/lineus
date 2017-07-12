from django import forms
from .models import Member, History, Schedule
from functools import partial

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('name','birth','phone_num','address','sex','type_choice','rating','period_fitness','period_pilates','period_both','locker','period_locker','cautions','exercise_time','visit_path','payment_amount','payment_method')



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