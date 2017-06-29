from django.contrib import admin
from staff.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin


# user = User.objects.create_user(Profile.name, Profile.email, Profile.password)

admin.site.register(Member)

