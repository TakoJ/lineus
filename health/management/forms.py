from django import forms
from django.contrib.auth.forms import UserChangeForm
from authentication.models import User
from management.models import FC_Teamleader_Commission, FC_Personal_Commission, FC_Team_Commission, Fitness_Teamledaer_Commission, Fitness_Personal_Commission, Pilates_Teamleader_Commission, Pilates_Commission
from staff.models import Member, History, Schedule

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class EditForm(forms.ModelForm):
    class Meta:
        model = Member
        fields= '__all__'

class FC_TeamLeader_EditForm(forms.ModelForm):
    class Meta:
        model = FC_Teamleader_Commission
        fields = '__all__'
