from django import forms
from .models import Member

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('name','birth','phone_num','address','sex','type_choice','rating','period_fitness','period_pilates','period_both','locker','period_locker','cautions','exercise_time','visit_path','payment_amount','payment_method')



class PT_RegisterForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('registered_session','PT_payment_amount','PT_payment_method','unitprice','period_PT')