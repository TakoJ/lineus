from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import Group
from authentication.models import User

class StaffRegisterForm(UserCreationForm): #usercreation inheritance
    SEX_CHOICES = [
        ('M','남자'),
        ('F','여자'),
    ]

    TEAM_CHOICES=[('FC','FC'),
                ('Fitenss','Fitness'),
                ('Pilates','Pilates')]
    sex = forms.ChoiceField(choices=SEX_CHOICES, widget=forms.RadioSelect())
    email = forms.EmailField()
    team = forms.ChoiceField(choices=TEAM_CHOICES, widget=forms.RadioSelect())
    teamleader = forms.BooleanField(required=False) #팀장여부

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'sex',
            'birth',
            'phone_num',
            'team',
            'teamleader',
            'basic_salary')

    def save(self, commit=True):
        user = super(StaffRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        team = self.cleaned_data['team']

        user.teamleader = self.cleaned_data['teamleader']

        if commit:
            user.save()
            user.groups.add(Group.objects.get(name=team))

        return user