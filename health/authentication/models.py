from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user')
    job = models.CharField(max_length=24)
    # job = forms.ChoiceField(choice=CHOICES, widget=forms.RadioSelect())
    def __str__(self):
        return str(self.user)

# Create your models here.
