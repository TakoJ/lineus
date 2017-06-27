from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from authentication.models import Profile

class SignupForm(UserCreationForm):
    #직업 선택
    CHOICES= (
        ('FC','FC'),
        ('PT','PT'),
        ('Pilates','Pilates'),
        ('CEO','CEO'),
    )

    job = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields

    def save(self):
        user = super().save()
        job = self.cleaned_data['job']
        Profile.objects.create(user=user, job=job)
        return user

