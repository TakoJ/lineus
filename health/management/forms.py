from django import forms
from django.contrib.auth.forms import UserChangeForm
from authentication.models import User
from staff.models import Member, History, Schedule

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class EditForm(forms.ModelForm):
    class Meta:
        model = Member
        fields= '__all__'
