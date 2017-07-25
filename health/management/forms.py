from django import forms
from django.contrib.auth.forms import UserChangeForm
from authentication.models import User
from management.models import FC_Teamleader_Commission, FC_Personal_Commission, FC_Team_Commission, Fitness_Teamledaer_Commission, Fitness_Personal_Commission, Pilates_Teamleader_Commission, Pilates_Commission, Pilates_GX_Basic, Pilates_GX_DependingNum, Pilates_PT
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

class FC_Team_EditForm(forms.ModelForm):
    class Meta:
        model = FC_Team_Commission
        fields = '__all__'

class FC_Personal_EditForm(forms.ModelForm):
    class Meta:
        model = FC_Personal_Commission
        fields = '__all__'

class Fit_TeamLeader_EditForm(forms.ModelForm):
    class Meta:
        model = Fitness_Teamledaer_Commission
        fields = '__all__'

class Fit_Personal_EditForm(forms.ModelForm):
    class Meta:
        model = Fitness_Personal_Commission
        fields = '__all__'

class Pil_TeamLeader_EditForm(forms.ModelForm):
    class Meta:
        model = Pilates_Teamleader_Commission
        fields = '__all__'

class Pil_Team_EditForm(forms.ModelForm):
    class Meta:
        model = Pilates_Commission
        fields = '__all__'

class Pil_GX_basic_EditForm(forms.ModelForm):
    class Meta:
        model = Pilates_GX_Basic
        fields = '__all__'

class Pil_DependingNum_EditForm(forms.ModelForm):
    class Meta:
        model = Pilates_GX_DependingNum
        fields = '__all__'

class Pil_PT_EditForm(forms.ModelForm):
    class Meta:
        model = Pilates_PT
        fields = '__all__'