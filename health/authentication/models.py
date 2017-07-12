from django.contrib.auth.models import User, AbstractUser
from django.db import models

# class Profile(models.Model):
#     user = models.OneToOneField(User, related_name='user')
#     job = models.CharField(max_length=24)
#     # job = forms.ChoiceField(choice=CHOICES, widget=forms.RadioSelect())
#     def __str__(self):
#         return str(self.user)

class User(AbstractUser):

    sex = models.CharField(max_length=12, verbose_name='성별',null=True)
    birth = models.DateField(null=True, blank=True)
    phone_num = models.CharField(max_length=32, null=True, help_text='Ex) 010-1234-1234',verbose_name='휴대번호')
    teamleader = models.BooleanField(blank=True, default=False, verbose_name='팀장 여부')
    basic_salary = models.DecimalField(max_digits=10, decimal_places=0, default=0 ,verbose_name='기본급')