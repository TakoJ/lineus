from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import Group
from authentication.models import User

class StaffRegisterForm(UserCreationForm): #usercreation inheritance
    SEX_CHOICES = [
        ('M','남자'),
        ('F','여자'),
    ]
    GX_CHOICES = [
        ('basic','기본'), #수업당 2만원
        ('depending_number','명수에 따라서')
    ]

    PT_CHOICES = [
        ('basic','매출당'), #매출당 수업료받는게 기본이니까.
        ('fix','고정된 비율') #현재 40%로 고정.
    ]
    TEAM_CHOICES=[('FC','FC'),
                ('Fitenss','Fitness'),
                ('Pilates','Pilates')]
    sex = forms.ChoiceField(choices=SEX_CHOICES, widget=forms.RadioSelect())
    email = forms.EmailField()
    team = forms.ChoiceField(choices=TEAM_CHOICES, widget=forms.RadioSelect())
    teamleader = forms.BooleanField(required=False) #팀장여부
    pilates_GX = forms.ChoiceField(choices=GX_CHOICES, widget=forms.RadioSelect(), required=False)
    pilates_PT = forms.ChoiceField(choices=PT_CHOICES, widget=forms.RadioSelect(), required=False)

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
            'pilates_GX',
            'pilates_PT',
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