from django import forms
from .models import Member, MembershipHistory, PaymentHistory, History, Pil_History, Schedule
from functools import partial

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('name','birth','phone_num','address','sex','registered_date', 'start_date', 'end_date', 'type_choice','rating','period_fitness','period_pilates','period_both', 'locker','locker_start_date', 'locker_end_date','cautions','exercise_time','visit_path','membership_amount','locker_amount','payment_amount','payment_method','note')

class Re_RegisterForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('phone_num','address','registered_date', 'start_date', 'end_date', 'type_choice','rating','period_fitness','period_pilates','period_both', 'locker','locker_start_date', 'locker_end_date','cautions','exercise_time','visit_path','membership_amount','locker_amount','payment_amount','payment_method','note')

class MembershipHistoryForm(forms.ModelForm):
    class Meta:
        model = MembershipHistory
        #registerform에서 name과 birth제외.
        fields = ('phone_num','address','sex','registered_date', 'start_date', 'end_date', 'type_choice','rating','period_fitness','period_pilates','period_both', 'locker','locker_start_date', 'locker_end_date','cautions','exercise_time','visit_path','membership_amount','locker_amount','payment_amount','payment_method','note')


#Fitness 등록, 히스토리
class PT_RegisterForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('registered_session','PT_payment_amount','PT_payment_method','unitprice','period_PT')

class PT_Register_HistoryForm(forms.ModelForm):
    class Meta:
        model = History
        fields = ('registered_session','PT_payment_amount','PT_payment_method','unitprice','period_PT')

#Pilates 등록, 히스토리
class Pil_RegisterForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('Pil_registered_session','Pil_payment_amount','Pil_payment_method','Pil_unitprice','Pil_period_PT')

class Pil_Register_HistoryForm(forms.ModelForm):
    class Meta:
        model = Pil_History
        fields = ('Pil_registered_session','Pil_payment_amount','Pil_payment_method','Pil_unitprice','Pil_period_PT')

class Schedule_AddForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ('title','start','end','Trainer')

class DateRangeForm(forms.Form):
    DateInput = partial(forms.DateInput, {'class': 'datepicker'})

    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())